from recipe_scrapers import scrape_me
import json
import extruct
import requests
import re
from w3lib.html import get_base_url
from bs4 import BeautifulSoup
import random
import time
from tqdm.notebook import tqdm

from . import db_funcs

class URLRetriever:
    """
    Class dedicated to retrieving URLS from recipe_scrapers supported websites.
    This class is used to get a list of recipe urls that will be fed into the scrape_unread_urls
    function. This will update the DB directly, so after scraping just run the scrape_unread_urls

    Usage:
    url_getter = URLRetriever()
    url_getter.Scrape(name='NAME_HERE')
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
                           'Food.com':self.scrape_food_com}


    def Scrape(self, name=None):
        """
        Run the scraper. See get_supported_retreiver_sites for eligible sites.
        Indiviual functions can be run without names.
        :param name: Website name for scraping
        :return:
        """
        if name in self.method_map.keys():
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

        source = 'epicurious'
        recipe_list = [x["_id"] for x in list(self.urls.find({"source": source}, {"_id": 1}))]

        for i in range(1, 2050):
            print(f"Page {i}/{2050}")
            wait()

            page = scrape_me(
                'https://www.epicurious.com/search/?content=recipe&sort=mostReviewed&page=' + str(i)).links()
            for link in page:
                if 'itemprop' in link.keys():
                    recipe = "https://www.epicurious.com" + link['href']
                    if recipe not in recipe_list:
                        self.urls.insert_one({"_id": recipe,
                                         "name": link['title'],
                                         'read': False,
                                         'type': [],
                                         'source': source,
                                         'website_id': link['href'].split("/")[-1].split("-")[-1],
                                         'react_id': link['data-reactid']})
                        recipe_list.append(recipe)
            print(f"Recipes Scraped: {len(recipe_list)}")

    def scrape_host_the_toast(self):

        source = 'host_the_toast'
        recipe_list = [x["_id"] for x in list(self.urls.find({"source": source}, {"_id": 1}))]
        page = scrape_me("https://hostthetoast.com/recipes/").links()
        categories = []

        # Some sites require category exploration to loop through recipes
        for link in page:
            if "category" in link["href"]:
                categories.append(link['href'])

        for c in categories:
            c_name = c.split("/category/")[1][:-1]
            for i in range(1, 40):
                page = scrape_me(c + "page/" + str(i)).links()

                if len(page) < 35:
                    break

                wait()
                for link in page:
                    if 'rel' in link.keys():
                        if "bookmark" in link["rel"]:
                            recipe = link['href']
                            if recipe not in recipe_list:
                                self.urls.insert_one({"_id": recipe,
                                                 "name": recipe.split("hostthetoast.com/")[1][:-1],
                                                 'read': False,
                                                 'type': [c_name],
                                                 'source': source})
                                recipe_list.append(recipe)
                print(f"Recipes Scraped: {len(recipe_list)}")

    def scrape_101_cookbooks(self):

        source = '101_cookbooks'
        recipe_list = [x["_id"] for x in list(self.urls.find({"source": source}, {"_id": 1}))]
        categories = ['https://www.101cookbooks.com/whole_grain_recipes',
                      'https://www.101cookbooks.com/wfpb',
                      'https://www.101cookbooks.com/vegetarian_recipes',
                      'https://www.101cookbooks.com/vegan_recipes',
                      'https://www.101cookbooks.com/soups',
                      'https://www.101cookbooks.com/sides',
                      'https://www.101cookbooks.com/sandwiches',
                      'https://www.101cookbooks.com/salads',
                      'https://www.101cookbooks.com/pasta',
                      'https://www.101cookbooks.com/quick_recipes',
                      'https://www.101cookbooks.com/main_courses',
                      'https://www.101cookbooks.com/low_carb_recipes',
                      'https://www.101cookbooks.com/instant_pot_recipes',
                      'https://www.101cookbooks.com/holiday_recipes',
                      'https://www.101cookbooks.com/high_protein_recipes',
                      'https://www.101cookbooks.com/gluten_free_recipes',
                      'https://www.101cookbooks.com/drink_recipes',
                      'https://www.101cookbooks.com/dinner_ideas',
                      'https://www.101cookbooks.com/desserts',
                      'https://www.101cookbooks.com/cookies',
                      'https://www.101cookbooks.com/chocolate_recipes',
                      'https://www.101cookbooks.com/breakfast_brunch',
                      'https://www.101cookbooks.com/baked_goods',
                      'https://www.101cookbooks.com/appetizers']

        for c in categories:
            c_name = c.split("/")[-1]
            for i in range(1, 40):
                page = scrape_me(c + "/page/" + str(i)).links()

                if len(page) > 198:
                    break

                wait()
                for j, link in enumerate(page[1:]):
                    if link['href'] == page[j]['href']:
                        recipe = link['href']

                        if recipe in recipe_list:
                            query = {"_id": recipe}
                            types = list(self.urls.find(query))[0]["type"]
                            if c_name not in types:
                                types.append(c_name)
                                self.urls.update_one(query, {"$set": {"type": types}})
                        else:
                            name = recipe
                            if "archives" in recipe:
                                name = recipe.split("/archives/")[1][:-5]
                            else:
                                name = recipe.split(".com/")[1][:-1]

                            self.urls.insert_one({"_id": recipe,
                                             "name": name,
                                             'read': False,
                                             'type': [c_name],
                                             'source': source})
                            recipe_list.append(recipe)
                print(f"Recipes Scraped: {len(recipe_list)}")

    def scrape_inspiralized(self):

        source = 'inspiralized'
        recipe_list = [x["_id"] for x in list(self.urls.find({"source": source}, {"_id": 1}))]

        for i in range(1, 60):
            page = scrape_me("https://inspiralized.com/recipe-index/page/" + str(i)).links()
            wait()
            for link in page:
                if "data-id" in link.keys():
                    recipe = link['href']
                    if recipe not in recipe_list:
                        self.urls.insert_one({"_id": recipe,
                                         "name": recipe.split(".com/")[1][:-1],
                                         'read': False,
                                         'type': [],
                                         'source': source,
                                         "website_id": link["data-id"]})
                        recipe_list.append(recipe)
            print(f"Recipes Scraped: {len(recipe_list)}")

    def scrape_jamie_oliver(self):

        source = 'jamie_oliver'
        recipe_list = [x["_id"] for x in list(self.urls.find({"source": source}, {"_id": 1}))]
        categories = [
            'https://www.jamieoliver.com/recipes/category/tesco-community-cookery-school/',
            'https://www.jamieoliver.com/recipes/category/dishtype/pasta-risotto',
            'https://www.jamieoliver.com/recipes/category/dishtype/salad/',
            'https://www.jamieoliver.com/recipes/category/dishtype/bread-doughs/',
            'https://www.jamieoliver.com/recipes/category/dishtype/curry/',
            'https://www.jamieoliver.com/recipes/category/dishtype/vegetable-sides/',
            'https://www.jamieoliver.com/recipes/category/dishtype/soup/',
            'https://www.jamieoliver.com/recipes/category/dishtype/antipasti/',
            'https://www.jamieoliver.com/recipes/category/dishtype/roast',
            'https://www.jamieoliver.com/recipes/category/dishtype/bbq-food/',
            'https://www.jamieoliver.com/recipes/category/dishtype/stews/',
            'https://www.jamieoliver.com/recipes/category/dishtype/pizza/',
            'https://www.jamieoliver.com/recipes/category/dishtype/sandwiches-wraps/',
            'https://www.jamieoliver.com/recipes/category/dishtype/cakes-tea-time-treats/',
            'https://www.jamieoliver.com/recipes/category/dishtype/pies-pastries/',
            'https://www.jamieoliver.com/recipes/category/dishtype/sauces-condiments/',
            'https://www.jamieoliver.com/recipes/category/dishtype/puddings-desserts/',
            'https://www.jamieoliver.com/recipes/category/dishtype/drinks/',
            'https://www.jamieoliver.com/recipes/cookie-recipes/',
            'https://www.jamieoliver.com/recipes/meatball-recipes/',
            'https://www.jamieoliver.com/recipes/muffin-recipes/',
            'https://www.jamieoliver.com/recipes/category/dishtype/pasta-bake/']

        for c in categories:
            c_name = c[:-1].split("/")[-1]
            for i in range(1, 60):
                page = scrape_me(c + "?rec-page=" + str(i)).links()

                if len(page) < 111:
                    break

                wait()
                for link in page:
                    if "id" in link.keys():
                        if "gtm_recipe" in link["id"]:
                            recipe = "https://www.jamieoliver.com" + link['href']

                            if recipe in recipe_list:
                                query = {"_id": recipe}
                                types = list(self.urls.find(query))[0]["type"]
                                if c_name not in types:
                                    types.append(c_name)
                                    self.urls.update_one(query, {"$set": {"type": types}})
                            else:
                                self.urls.insert_one({"_id": recipe,
                                                 "name": recipe[:-1].split("/")[-1],
                                                 'read': False,
                                                 'type': [c_name],
                                                 'source': source})
                                recipe_list.append(recipe)
                print(f"Recipes Scraped: {len(recipe_list)}")

    def scrape_kreme_de_la_krum(self):

        source = 'creme_de_la_crum'
        recipe_list = [x["_id"] for x in list(self.urls.find({"source": source}, {"_id": 1}))]

        for i in range(1, 53):
            page = scrape_me("https://www.lecremedelacrumb.com/recipe-index//page/" + str(i)).links()
            wait()
            for link in page:
                for link in page:
                    if 'rel' in link.keys():
                        if "bookmark" in link["rel"]:
                            recipe = link['href']
                            if recipe not in recipe_list:
                                self.urls.insert_one({"_id": recipe,
                                                 "name": recipe.split(".com/")[1][:-1],
                                                 'read': False,
                                                 'type': [],
                                                 'source': source, })
                                recipe_list.append(recipe)
            print(f"Recipes Scraped: {len(recipe_list)}")

    def scrape_minamlist_baker(self):

        source = 'minamalist_baker'
        recipe_list = [x["_id"] for x in list(self.urls.find({"source": source}, {"_id": 1}))]

        for i in range(1, 63):
            page = scrape_me("https://minimalistbaker.com/recipe-index/?fwp_paged=" + str(i)).links()
            wait()
            for link in page:
                for link in page:
                    if 'tabindex' in link.keys():
                        recipe = link['href']
                        if recipe not in recipe_list:
                            self.urls.insert_one({"_id": recipe,
                                             "name": recipe.split(".com/")[1][:-1],
                                             'read': False,
                                             'type': [],
                                             'source': source, })
                            recipe_list.append(recipe)
            print(f"Recipes Scraped: {len(recipe_list)}")

    def scrape_food_com(self):

        # Build Topic List
        try:
            topic_file = open('./scraped_urls/food_com_topics.json')
            topics = json.load(topic_file)
        except:
            topics = {}
            alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                        't', 'u', 'v', 'w', 'x', 'y', 'z']

            for letter in alphabet:
                path = 'https://www.food.com/topic/' + letter
                topics[letter] = {}
                wait()

                for link in scrape_me(path).links():
                    if 'topic/' in link['href']:
                        topics[letter][link['href']] = 1

            with open('./scraped_urls/food_com_topics.json', 'w') as json_file:
                json.dump(topics, json_file)

        # Loop through topics and grab num_pages for topic
        num_pages = 12
        for letter in topics:
            for topic in topics[letter]:

                c_name = topic.split('www.food.com/topic/')[1]
                if topics[letter][topic] == 'end':
                    print(topic + " is Complete.")
                    continue
                else:
                    start = topics[letter][topic]
                    stop = topics[letter][topic] + num_pages

                    print("Scraping " + topic + " From " + str(start) + " to " + str(stop))
                    for i in range(topics[letter][topic], topics[letter][topic] + num_pages):
                        wait()
                        page = scrape_me(topic + "?pn=" + str(i)).links()

                        if len(page) < 40:
                            topics[letter][topic] = 'end'
                            break
                        else:
                            for link in page:
                                if 'recipe/' in link['href']:
                                    recipe = link['href']

                                    # Insert checks
                                    if recipe in self.recipes:
                                        types = list(self.urls.find({"_id": recipe}, {"_id": 0, "type": 1}))[0]['type']
                                        if c_name not in types:
                                            types.append(c_name)
                                            query = {"_id": recipe}
                                            newvalues = {"$set": {"type": types}}
                                            self.urls.update_one(query, newvalues)

                                    else:
                                        self.urls.insert_one({'_id': recipe,
                                                         'name': "-".join(recipe.split("/")[-1].split("-")[:-1]),
                                                         'read': False,
                                                         'type': [c_name],
                                                         'source': 'food_com',
                                                         'website_id': recipe.split("/")[-1].split("-")[-1]})
                                        self.recipes.append(recipe)

                            # Save incrementally to avoid not counting progress
                            topics[letter][topic] += 1
                            with open('./scraped_urls/food_com_topics.json', 'w') as json_file:
                                json.dump(topics, json_file)
                print(f"Total Scraped at {len(self.recipes)}.")
                print(f"Total in Database at {len(list(self.urls.find({'source': 'food_com'})))}.")

class RecipeCollector:

    def __init__(self, url, domain, source, utm_pages=False):
        """
        :param url: The URL to start the crawler on
        :param domain: Domain of the URL to check which links link off the site
        :param source: DB name for this source
        :param utm_pages: Bool for whether pagination occurs within utm parameters
        """
        # User Params
        self.base_url = url
        self.domain = domain
        self.source = source
        self.rdb = db_funcs.get_scraper_dbs()[1]
        self.sdb = db_funcs.get_source_ref()
        self.utm_pages = utm_pages

        # Scraping Defaults
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7"}

        # Dictionaries for checking links (avoiding redundancy)
        if len(list(self.sdb.find({"_id": source}))) > 0:
            src_ref = list(self.sdb.find({"_id": source}))[0]
            self.link_library = src_ref["link_library"]
            self.scraped_recipes = src_ref["scraped_recipes"]
        else:
            self.link_library = {}
            self.scraped_recipes = []
            self.sdb.insert_one({"_id": source,
                                 "link_library": self.link_library,
                                 "scraped_recipes": self.scraped_recipes})

    # Helper Functions
    def recursive_page_scrape(self, page):
        """
        Crawls across website and scrapes recipes as discovered.
        The navigation is recursive, scraping each page it comes upon and all the links
        on that page.
        """
        # Mark as being read
        print_message = f"Recipes Found: {len(self.scraped_recipes)} | Scraping {page}"
        print(print_message.ljust(200, " "), end="\r", flush=True)
        self.link_library[page] = 1
        self.sdb.update_one({"_id": self.source}, {"$set": {"link_library": self.link_library}})

        # Scrape it, if it errors out it won't be tried again
        r = requests.get(page, headers=self.headers)
        soup = BeautifulSoup(r.content, "html.parser")
        base_url = get_base_url(r.text, r.url)
        data = extruct.extract(r.text, base_url=base_url)

        # Recipe
        self.scrape_recipe(data, page)

        # Look for all links on page
        for link_string in soup.findAll('a', attrs={'href': re.compile("^https://")}):
            link = clean_url(link_string.get('href'), self.utm_pages)
            if check_link(link, self.domain):
                if link not in self.link_library.keys():
                    wait()
                    self.recursive_page_scrape(link)

    def scrape_recipe(self, link_data, page):
        """
        Checks if given link_data contains a recipe and scrapes if it does.
        """
        if page not in self.scraped_recipes:
            recipe = {}
            self.recursive_recipe_lookup(link_data, recipe)

            if len(recipe) == 0:
                return False
            else:
                self.add_scraped_recipe(recipe["recipe_data"])
                self.scraped_recipes.append(page)
                self.sdb.update_one({"_id": self.source}, {"$set": {"scraped_recipes": self.scraped_recipes}})
                return True
        else:
            return False

    def recursive_recipe_lookup(self, data, recipe):
        for key, value in data.items():
            if key == "@type":
                if value == "Recipe":
                    recipe["recipe_data"] = data
            if type(value) == type(dict()):
                self.recursive_recipe_lookup(value, recipe)
            elif type(value) == type(list()):
                for val in value:
                    if type(val) == type(str()):
                        pass
                    elif type(val) == type(list()):
                        pass
                    elif type(val) == type(tuple()):
                        pass
                    else:
                        self.recursive_recipe_lookup(val, recipe)

    def add_scraped_recipe(self, recipe_data):
        """
        Takes a schema.org scraped recipe, formats it and adds to database.
        """
        row = {}

        # Source
        row["source"] = self.source

        # Title
        row['title'] = recipe_data["name"] if "name" in recipe_data.keys() else None

        # Description
        row['description'] = recipe_data["description"] if "description" in recipe_data.keys() else None

        # Author
        row["author"] = recipe_data["author"]["name"] if "author" in recipe_data.keys() else None

        # Ingredients
        row["ingredients"] = recipe_data["recipeIngredient"] if "recipeIngredient" in recipe_data.keys() else None

        # url
        row["url"] = recipe_data["url"] if "url" in recipe_data.keys() else None

        # Times
        row["prepTime"] = recipe_data["prepTime"] if "prepTime" in recipe_data.keys() else None
        row["cookTime"] = recipe_data["cookTime"] if "cookTime" in recipe_data.keys() else None
        row["totalTime"] = recipe_data["totalTime"] if "totalTime" in recipe_data.keys() else None

        # Date Published (left in format)
        row["datePublished"] = recipe_data["datePublished"] if "datePublished" in recipe_data.keys() else None

        # Yields
        row["recipeYield"] = return_as_list(recipe_data["recipeYield"])[
            0] if "recipeYield" in recipe_data.keys() else None

        # Category
        row["recipeCategory"] = return_as_list(
            recipe_data["recipeCategory"]) if "recipeCategory" in recipe_data.keys() else None

        # Cooking Method
        row["cookingMethod"] = return_as_list(
            recipe_data["cookingMethod"]) if "cookingMethod" in recipe_data.keys() else None

        # Cuisine
        row["recipeCuisine"] = return_as_list(
            recipe_data["recipeCuisine"]) if "recipeCuisine" in recipe_data.keys() else None

        # Ratings
        if 'aggregateRating' in recipe_data.keys():
            row["rating"] = recipe_data["aggregateRating"]["ratingValue"] if "ratingValue" in recipe_data[
                "aggregateRating"].keys() else None
            row["review_count"] = recipe_data["aggregateRating"]["reviewCount"] if "reviewCount" in recipe_data[
                "aggregateRating"].keys() else None
        else:
            row["rating"] = None
            row["review_count"] = None

        # Reviews (unstructured)
        row["reviews"] = recipe_data["review"] if "review" in recipe_data.keys() else None

        # Instructions
        if "recipeInstructions" in recipe_data.keys():
            try:
                row["instructions"] = [x['text'] for x in recipe_data["recipeInstructions"]]
            except:
                row["instructions"] = recipe_data["recipeInstructions"]
        else:
            row["instructions"] = None

        # Keywords
        if "keywords" in recipe_data.keys():
            row["keywords"] = [x for x in recipe_data["keywords"].split(",")]
        else:
            row["keywords"] = None

        # Write into database
        self.rdb.insert_one(row)

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

# Helper Functions
def wait():
    """
    Random amount of time to wait to avoid overloading a website
    :return:
    """
    x = random.randrange(50, 200, 1) / 100
    print(f"Waiting for {x} Seconds.", end='\r')
    time.sleep(x)

def split_time(t):
    clean_t = t[2:]
    if 'H' in clean_t:
        split = clean_t.split("H")
        hours = split[0]
        minutes = split[1][:-1]
        return (60 * int(hours)) + int(minutes)
    else:
        minutes = clean_t[:-1]
        return int(minutes)

def return_as_list(x):
    if type(x) == type(list()):
        return x
    else:
        return [x]

def clean_url(x, utm_pages=False):
    clean = x
    if "#" in clean:
        clean = clean.split("#")[0]
    if not utm_pages:
        if "?" in clean:
            clean = clean.split("?")[0]
            return clean
    return clean

def check_link(link, domain):
    stopwords = [".jpg", ".png", "wprm_print", "wprm-print", "wp-content", "comment-page"]

    if not link.startswith(domain):
        return False
    for word in stopwords:
        if word in link:
            return False
    return True