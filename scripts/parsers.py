import ast

class IngredientParser:
    """
    A Parser for processing ingredients
    """
    def __init__(self):
        """
        No params needed, intialization setsup many of the variables needed to run the main function
        .Parse(). This class is only half-baked, it contains a crude and static ingredient reference
        but would need to be widely expanded for general use.
        """
        self.units = ["cup", "c." "g", "gram", 'lb', 'teaspoon', "tsp", "tbsp", "oz", 'tablespoon', 'container', 'packet',
                 'bag',
                 "stick",
                 'quart', 'pound', 'can', 'bottle', 'pint', 'package', 'ounce', 'jars', 'heads', 'gallons', 'drops',
                 "drop",
                 'envelope', 'bar', 'box', 'pinch', 'dash', 'bunch', 'recipe', 'layer', 'slice', 'link', 'bulb',
                 'stalk',
                 'square', 'sprig',
                 'fillet', 'piece', 'leg', 'thigh', 'cube', 'granule', 'strip', 'tray', 'leave', 'loaves', 'halves',
                 'jar']

        self.descriptors = ['beaten', 'chopped', 'cold', 'diced', 'packed', 'hot', 'large', 'melted', 'mini',
               'miniature', 'packed', 'room temperature', 'sifted', 'softened', 'warm', "drained", "rinsed", "optional",
               "mashed", "ripe", "medium", "ground", "pitted", "ground"]

        self.ir = {
                  "flour":{
           "types":['all purpose', "white", "brown", "spelt", "oat", "millet",
                 "whole wheat", "almond", "tapioca", "sorghum", "rice", "coconut", "garfava"
                 "barley", "cake", "bread", "self-rising", "soy", "pastry"]
                  },
                  "brown sugar":{
                      "types":["dark", "light"],
                      "aka":["brown-sugar"]
                  },
                  "sugar":{
                      "types":["granulated", "white", "substitute", "splenda", "cane"],
                      "aka":["splenda"],
                      "stopwords":["free"]
                  },
                  "butter":{
                      "types":["salted", "unsalted"],
                      "stopwords":["almond", "peanut", "scotch"]
                  },
                  "water":{
                      "types":[]
                  },
                  "baking powder":{
                      "types":[],
                      "aka":["baking-powder"]
                  },
                  "salt":{
                      "types":["kosher", "coarse", "sea", "popcorn", "fine", "himalayan", "table"],
                      "aka":["sea-salt"]
                  },
                  "chocolate chip":{
                      "types":["semi sweet", "milk", "dark", "white", "bittersweet"],
                      "aka":["chocolate chips"]
                  },
                  "chocolate chunk":{
                      "types":["semi sweet", "milk", "dark", "white", "bittersweet"],
                      "aka":["chocolate chunks", "chocolate morsels", "chocolate morsel"]
                  },
                  "baking soda":{
                      "types":[],
                      "aka":["baking-soda"]
                  },
                  "oat":{
                      "types":["old fashioned", "rolled", "quick-cooking"],
                      "aka":["rolled-oats"],
                      "stopwords":["milk", 'flour']
                  },
                  "vanilla extract":{
                      "types":['madagascar'],
                      "aka":["vanilla"]
                  },
                  "shortening":{
                      "types":['vegatable']
                  },
                  "walnut":{
                      "types":["roasted", "toasted"],
                      "aka":["walnuts"],
                      "stopwords":[" nuts"]
                  },
                  "pecan":{
                     "types":["roasted", "toasted"],
                     "aka":["pecans" ]
                  },
                  "oil":{
                      "types":["olive", "vegetable", "avocado", "canola", "virgin", "coconut"]
                  },
                  "coconut":{
                      "types":["flaked", "unsweetened"],
                      "stopwords":["milk", "pudding"]
                  },
                  "chickpeas":{
                      "types":[],
                      "aka":["garbonzo beans", "ghana"]
                  },
                  "cooking spray":{
                      "types":["nonstick"],
                      "aka":["pam"]
                  },
                  "milk":{
                      "types":["whole", "2%", "skim", "dairy free", "coconut", "almond", "oat", "soy"]
                  },
                  "sour cream":{
                      "types":["fat free", "dairy free"]
                  },
                  "banana":{
                      "types":["cavendish"],
                      "stopwords":["extract"]
                  },
                  "banana extract":{
                      "types":[]
                  },
                  "cornstarch":{
                      "types":[]
                  },
                  "cocoa powder":{
                      "types":[]
                  },
                  "nuts":{
                      "types":["walnut", "pecan", "peanut"]
                  },
                  "peanut":{
                      "types":[],
                      "stopwords":[" nuts", "butter"]
                  },
                  "honey":{
                      "types":[]
                  },
                  "baking mix":{
                      "types":[]
                  },
                  "cherry":{
                      "types":[],
                      "aka":["cherries"]
                  },
                  "almond extract":{
                      "types":[]
                  },
                  "almond":{
                      "types":[],
                      "stopwords":["milk", "extract"]
                  },
                  "pudding":{
                      "types":["coconut cream", "butterscotch"]
                  },
                  "heavy cream":{
                      "types":[]
                  },
                  "pretzels":{
                      "types":[]
                  },
                  "date":{
                      "types":["medjool"]
                  },
                  "flax seeds":{
                      "types":[]
                  },
                  "quinoa":{
                      "types":[]
                  },
                  "applesauce":{
                      "types":[]
                  },
                  "xanthan gum":{
                      "types":[]
                  },
                  "cinnamon":{
                      "types":["ground", "saigon"]
                  },
                  "instant coffee":{
                      "types":[]
                  },
                  "peanut butter":{
                      "types":[]
                  }
                }

    def Parse(self, ing):
        """
        Core function for processing an ingredient
        :param ing:
        :return:
        """

        # Output schema for parsing
        ing_dict = {"ingredient_string": ing.lower(),
                    "quant": None,
                    "unit": None,
                    "item": None,
                    "type": None,
                    "descriptors": None}
        split_ing = ['None', 'None']

        # Unit Parsing
        for unit in self.units:
            if " " + unit + "s " in ing:
                ing_dict["unit"] = unit
                split_ing = ing.lower().split(" " + unit + "s ")
                break
            elif " " + unit + "es " in ing:
                ing_dict["unit"] = unit
                split_ing = ing.lower().split(" " + unit + "es ")
                break
            elif " " + unit + " " in ing:
                ing_dict["unit"] = unit
                split_ing = ing.lower().split(" " + unit + " ")
                break
            else:
                continue
        ing_dict["quant"] = self.parse_quant(split_ing[0])

        # ING Parsing
        ing_dict["item"] = self.parse_ing_item(split_ing[1])
        ing_dict["type"] = self.parse_ing_types(split_ing[1], ing_dict["item"])
        ing_dict["descriptors"] = self.parse_ing_descriptors(split_ing[1])

        # Special
        if "egg" in ing:
            ing_dict['item'] = "egg"
            ing_dict["unit"] = "eggs"
            ing_dict["quant"] = self.parse_quant(ing.split(" ")[0])

        return ing_dict

    def parse_quant(self, quant):
        """
        Parse out a numerical quantity from fractional and other representations
        :param quant: str containing quantity to conver
        :return: float of quantity
        """
        if quant is None:
            return 0

        fractions = {"↉": "0", "⅒": "1/10", "⅑": "1/9", "⅛": "1/8",
                     "⅐": "1/7", "⅙": "1/6", "⅕": "1/5", "¼": "1/4",
                     "⅓": "1/3", "½": "1/2", "⅖": "2/3", "⅔": "2/3",
                     "⅜": "3/8", "⅗": "3/5", "¾": "3/4", "⅘": "4/5",
                     "⅝": "5/8", "⅚": "5/6", "⅞": "7/8"}

        new_quant = quant.replace("⁄", "/")
        for frac in fractions:
            if frac in quant:
                new_quant.replace(frac, fractions[frac])

        quant_num = 0
        for num in new_quant.split(" "):
            try:
                if "/" in num:
                    try:
                        quant_num += ast.literal_eval(num.split("/")[0]) / ast.literal_eval(num.split("/")[1])
                    except:
                        quant_num += 0
                elif ("-" in num) | ("to" in num):
                    break
                else:
                    quant_num += ast.literal_eval(num)
            except:
                quant_num += 0

        return quant_num

    def parse_ing_descriptors(self, ing_string):
        """
        Loop through possible descriptors for an ingredient and pull them out into a list
        :param ing_string:
        :param descriptors:
        :return:
        """

        descriptors_found = []
        for desc in self.descriptors:

            if desc in ing_string:
                descriptors_found.append(desc)
            elif " " in desc:
                if "-".join(desc.split(" ")) in ing_string:
                    descriptors_found.append(desc)

        return descriptors_found

    def parse_ing_types(self, ing_string, item):
        """
        Parse out the ingredient types for an ingredient string using regex
        :param ing_string: str of ingredient for a recipes ingredient list
        :param item: the item in ir to which the ingredient belongs
        :return: List of types the ingredient matches
        """
        found_types = []
        if item not in self.ir.keys():
            return found_types

        for ing_type in self.ir[item]["types"]:

            if ing_type in ing_string:
                found_types.append(ing_type)
            elif " " in ing_type:
                if "-".join(ing_type.split(" ")) in ing_string:
                    found_types.append(ing_type)

        return found_types

    def parse_ing_item(self, ing_string):
        """
        Determine which item the ingredient is using ir
        :param ing_string: ingredient string to look for
        :return: the item from ir the ingredient corresponds to
        """
        for item in self.ir:

            # Item name
            if item in ing_string:
                good_match = True

                # Check if stopwords
                if "stopwords" in self.ir[item]:
                    for sw in self.ir[item]["stopwords"]:
                        if sw in ing_string:
                            good_match = False

                if good_match:
                    return item
                else:
                    continue

            elif "aka" in self.ir[item].keys():
                for name in self.ir[item]["aka"]:
                    if name in ing_string:
                        return item


def parse_recipe_ingredients(ing_list):
    """
    A function that leverages the parser class to process an entire list
    :param ing_list:
    :return:
    """
    parsed = []
    ip = IngredientParser()

    for x in ing_list:
        parsed.append(ip.Parse(x))

    return parsed



