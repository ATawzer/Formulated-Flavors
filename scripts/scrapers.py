import pandas as pd
from recipe_scrapers import scrape_me
import time
import random
import json
import pymongo
from tqdm.notebook import tqdm
import numpy as np

def wait():
    """
    Random amount of time to wait to avoid overloading a website
    :return:
    """
    x = random.randrange(50, 200, 1) / 100
    print(f"Waiting for {x} Seconds.", end='\r')
    time.sleep(x)

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