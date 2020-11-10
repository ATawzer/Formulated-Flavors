import pandas as pd
from recipe_scrapers import scrape_me
import time
import random
import json
import pymongo
from tqdm.notebook import tqdm
import numpy as np

from . import db_funcs

def wait():
    """
    Random amount of time to wait to avoid overloading a website
    :return:
    """
    x = random.randrange(50, 200, 1) / 100
    print(f"Waiting for {x} Seconds.", end='\r')
    time.sleep(x)

class URLRetriever:
    """
    Class dedicated to retrieving URLS from recipe_scrapers supported websites.
    This class is used to get a list of recipe urls that will be fed into the scrape_unread_urls
    function. This will update the DB directly, so after scraping just run the scrape_unread_urls
    """
    def __init__(self):
        self.urls, self.recipes = db_funcs.get_scraper_dbs()

        self.method_map = {'Epicurious':self.scrape_epicurious,
                           'Host the Toast':self.scrape_host_the_toast,
                           '101 Cookbooks':self.scrape_101_cookbooks,
                           'Inspiralized':self.scrape_inspiralized,
                           'Jamie Oliver':self.scrape_jamie_oliver,
                           'Kreme de la Krum':self.scrape_kreme_de_la_krum,
                           'Minimalist Baker':self.scrape_minamlist_baker,
                           'Next One':self.scrape_next_one,
                           'Food.com':self.scrape_food_com}


    def Scrape(self, name=None):
        """
        Run the scraper. See get_supported_retreiver_sites for eligible sites.
        Indiviual functions can be run without names.
        :param name: Website name for scraping
        :return:
        """
        if name in self.method_map:
            self.method_map[name]()
        else:
            return "Website not Supported."

    def get_supported_retreiver_sites(self):
        """
        Print eligible sites
        :return: None
        """
        print(self.method_map.keys())

    # Functions per site
    def scrape_epicurious(self):
        

def scrape_unread_urls(urls, recipes):
    """
    Urls that have been marked as unread within the urls database
    :param urls: Pymongo DB storing urls to be scraped (must be compatible with scrape_me)
    :param recipes: Pymongo DB to insert recipes once they have been scraped
    :return: None, can be stopped mid process
    """

    # Obtain list of urls to scrape over
    eligible_urls = [x["_id"] for x in list(urls.find({"read": False, "error":False}, {"_id": 1}))]
    eligible_urls = sorted(eligible_urls, key=lambda x: random.random())

    if len(eligible_urls) == 0:
        print("No URL's to Read.")
        return None

    for url in tqdm(eligible_urls):

        # Obtain existing data
        print(url)
        row = list(urls.find({"_id": url}))[0]

        try:
            if url[0] != 'h':
                url = "https:" + url

            # Pause and then scrape
            wait()
            scraper = scrape_me(url)

            # Attempt each piece of data
            # Title
            try:
                title = scraper.title()
            except:
                try:
                    title = row['name']
                except:
                    title = None

            # Total Time
            try:
                total_time = scraper.total_time()
            except:
                total_time = None

            # Yields
            try:
                yields = scraper.yields()
            except:
                yields = None

            # Ingredients
            try:
                ingredients = scraper.ingredients()
            except:
                ingredients = []

            # Instructions
            try:
                instructions = scraper.instructions().encode('utf-8', 'surrogatepass')
            except:
                instructions = None

            # Image
            try:
                image = scraper.image()
            except:
                image = None

            # Ratings
            try:
                rating = scraper.ratings()
            except:
                rating = None

            # Author
            try:
                author = scraper.author()
            except:
                try:
                    author = row['author']
                except:
                    author = None

            # Reviews
            try:
                reviews = scraper.reviews()
            except:
                reviews = None

            # Insert new data
            recipes.insert_one({"title": title,
                                "total_time": total_time,
                                "yields": yields,
                                "ingredients": ingredients,
                                "instructions": instructions,
                                "image": image,
                                "rating": rating,
                                "author": author,
                                "reviews": reviews,
                                "source": row['source'],
                                "url": row["_id"]})

            # Mark as read
            query = {"_id": url}
            newvalues = {"$set": {"read": True}}
            urls.update_one(query, newvalues)

        except:

            # Mark as Error
            print("Error encountered.")
            query = {"_id": url}
            newvalues = {"$set": {"error": True}}
            urls.update_one(query, newvalues)