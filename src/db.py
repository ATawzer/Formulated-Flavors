from pymongo import MongoClient
from dotenv import load_dotenv
import json
import os
import pandas as pd

load_dotenv()

class FormulatedFlavorsDB:
    """
    Class for managing MongoDB connection to Formulated Flavors DB
    """

    def __init__(self):

        self.mc = MongoClient(os.getenv('mongo_host'),
                             username=os.getenv('mongo_user'),
                             password=os.getenv('mongo_pass'),
                             authSource=os.getenv('mongo_auth_db'),
                             authMechanism='SCRAM-SHA-256')
        self.db = self.mc[os.getenv('mongo_db')]

        # Collections
        self.recipes = self.db['recipes']

    # Recipes
    def get_recipes_by_search_title(self, title):
        """
        Attempts to obtain recipes where the name is included
        in a regex search on title.
        """
        q = {"title":{"$regex":title, "$options": "-i"}}
        cols = {"_id":1}
        r = list(self.recipes.find(q, cols))

        if len(r) == 0:
            print("No recipes found for given query.")
            return r
        else:
            return [x["_id"] for x in r]

    def get_recipe_ingredients(self, recipe_ids):
        """
        Returns all ingredients from the specified recipes as list
        """
        q = {"_id":{"$in":recipe_ids}}
        cols = {"ingredients":1}
        r = list(self.recipes.find(q, cols))

        return [x["ingredients"] for x in r]

    def get_recipes(self, recipe_ids, fields={}):
        """
        Generic Recipe endpoint for getting all recipe data
        """
        q = {"_id":{"$in":recipe_ids}}
        cols = fields
        r = list(self.recipes.find(q, cols))

        return r