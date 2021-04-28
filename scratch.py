from src.db import FormulatedFlavorsDB
import pandas as pd

ffdb = FormulatedFlavorsDB()

def gen_ingredient_report_by_search_title(query):

    recipes = ffdb.get_recipes_by_search_title(query)
    recipe_info = ffdb.get_recipes(recipes, fields={"_id":1, "title":1, "ingredients":1, "source":1, "url":1})
    ingredients = ffdb.get_recipe_ingredients(recipes)

    with open(f"data/ingredient_report - {query}.txt", "w") as output:

        for i, recipe in enumerate(recipe_info):
            output.write(f"==== {recipe['source']} | {recipe['title']} ====\n")
            output.write(f"{recipe['url']}\n\n")

            for j, ing in enumerate(ingredients[i]):
                output.write(f"{ing}\n")
            output.write("\n")

gen_ingredient_report_by_search_title('lemon bundt cake')