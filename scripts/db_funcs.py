import pandas as pd
from recipe_scrapers import scrape_me
import time
import random
import json
import pymongo
from tqdm.notebook import tqdm
import numpy as np

# Db Information
def get_scraper_dbs():
    """
    Assuming the DB has been setup, return the urls and recipes database for scraping
    :return:
    """
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['food_analysis']
    urls = db['urls']
    recipes = db['recipes']
    return urls, recipes

def get_source_ref():
    """
    Get a list of sources from the database
    :return:
    """
    # Database setup
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client['food_analysis']
    return db['source_ref']

def print_db_metadata(urls, recipes):
    """
    Easy way to obtain some basic information about the recipes and urls
    :param urls: Pymongo DB storing urls to be scraped (must be compatible with scrape_me)
    :param recipes: Pymongo DB to insert recipes once they have been scraped
    :return: Print statements
    """

    # Print Overview
    total = len(list(urls.find({})))
    read = len(list(urls.find({"read": True})))
    togo = len(list(urls.find({"read": False})))
    errors = len(list(urls.find({"error": True})))
    in_recipes = len(list(recipes.find({})))

    print(f"URL Database: {total}")
    print(f"Read: {read}")
    print(f"To Read: {togo}")
    print(f"Errors: {errors}")
    print(f"Recipes Database: {in_recipes}")

def recipes_clean_duplicates(recipes):
    """
    Cleanup duplicates in the recipes database
    :param recipes: Recipes DB for already scraped recipes
    :return: None, will update the DB directly
    """

    # Remove Duplicates (true dups, everything is identical)
    dups = pd.DataFrame(list(recipes.find({})))
    dups = dups[["_id", "url"]].groupby("url", as_index=False).count()
    dups = np.unique(dups[dups["_id"] > 1]["url"])
    for url in dups:
        delete = [x["_id"] for x in list(recipes.find({"url": url}))[1:]]
        for did in delete:
            recipes.delete_one({"_id": did})

def clean_read_recipe_urls(urls, recipes):
    """
    Check for already processed recipes and update their read flag
    :param urls: URLs DB
    :param recipes: Recipes DB
    :return: None, will update the DB directly
    """

    read_urls = [x["url"] for x in list(recipes.find({}))]
    for url in tqdm(read_urls):
        urls.update_one({"_id": url}, {"$set": {"read": True, "error": False}})