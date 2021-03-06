﻿# Formulated Flavors
The code and analysis tools behind the website formulatedflavors.com, a food blog exploring data-driven recipe creation and perfection. Using a collection of web scrapers, nearly 250,000 recipes have been pulled from the best recipe sites and food blogs from across the internet. By analyzing staple foods, like a chocolate chip cookie, across so many recipe creators the hope is to find the optimal recipe. Formulated Flavors, then, is the data-backed compression of an internet’s worth of recipes into a small set of well-designed recipes.

The code in this repository focuses on 3 functions: Scraping, Parsing and Analyzing. Scraping offers quick functions that allow for mass recipe gathering with very little knowledge of the recipe sites and minimal work upfront for the user. Parsing allows for the processing of the recipes into more machine-readable formats. Analysis employs the newly acquired and structured data to find the best ways to make or improve a recipe.

# Scripts – Building and Parsing a Recipe Database 
There are two major sources of recipes: recipe sites and food blogs. Sites like AllRecipes.com or Food.com are good examples of a recipe site. They contain large amounts of recipes submitted by a large user base. Food blogs on the other hand are typically a single author creating many recipes and provide more information (pictures, anecdotes, etc.) around the recipes. While it was attempting to let the bulk of the recipes come from a single few sources and recipe sites for technical simplicity, it was important that food blogs were well represented. Food blogs have many of the high-quality and well-crafted recipes that circulate through Pintrest and Yummly. To ensure that the optimal recipe exists as the aggregate of the recipes in the database it was important to have the perfect mix recipe types.

## scrapers.py
There are two methods in the scraping methodology. One was to leverage an existing recipe scraping package (see the requirements section) with pre-built hooks into some of the most popular recipe sites and a few well-known food blogs. The second is a food-blog agnostic approach which leverages a popular WordPress recipe format that a large chunk of food blogs use now or have switched to using recently. While paging through a food blog is slower, it is extremely easy to setup and allows the seamless integration of many different sources (assuming they use WordPress).

The information obtained from scraping is written directly to the mongoDB to be accessed in the parsing and analysis steps.

URLRetriever: A static method for obtaining a list of recipe urls for scraping from a few pre-defined sources. The supported sites can be accessed from the class object and recipe urls can be scraped with .Scrape() and the name of the site. Once the urls are scraped the scrape_unread_recipe_urls() function must be called and the recipes will be obtained. 

RecipeCollector: A web-crawler object for recursively scraping an entire food blogs catalog of recipes. All that is needed to spin a crawler up is the starting page and some DB tagging. This works by recursively exploring every link on a website and tracking which pages have been visited. If the crawler comes across a page where it finds the wordpress recipe format, it will scrape it. This makes it very clean to get a consistent data feed from each food blog and get a full set of recipes without having to specify the individual food blog’s page structure.

## db_funcs.py
To avoid writing lots of information and sharing it in flat files the scrapers and parsers scripts talk directly to a mongoDB database. The db_func.py provides the tools for interfacing with this database but does not contain an easy way to setup the database in the first place. The main goal of these functions is to eliminate needing to handoff recipes from different functions in parsers and scrapers. Instead, they both can reference db_funcs.py which will obtain the database links for them to update the underlying shared data directly.

## parsers.py
This is where the room for most work is possible. Currently, the only parsing that occurs is on the ingredients, though it will need to be expanded to include instructions at the very least. The challenge is that while the data is structured uniformly on writing to the database, the data itself is a messy mix of humans. There are hundreds of ways to write the amount of flour needed for a recipe and its very tedious to consolidate this information into a machine-readable format. The initial approach was to use a regex parser designed to look specifically for certain pieces of information store in self.ir (Ingredient Reference). However, given the vast number of possible ingredients and even more ways to write them it is obvious this approach is not feasible.

Other approaches include using train/test datasets from sources like NYT cooking to use machine learning and NLP approaches to an effective mapping of messy ingredient -> machine-readable ingredients. Additionally, there are ingredient parsing libraries that could be leveraged for some less effort manual parsing. A combination of these approaches and some band-aids will likely be required for a usable and consistent output.

Once the parsing is figured out the project will function like an application, ready to take in a recipe and spit out analysis on improvements.

# Notebooks – A scraping and analysis interface
The notebooks for this project function as a simpler code interface. The work is done by the scripts, but orchestrating which scripts and blogs to obtain is done in a notebook.

## Recipe Scraping.ipynb
If it involves getting the recipe information from the internet it happens here. Some of the feeds from existing blogs I used to create my own database are in the notebook. Example usage of the scrapers and db_funcs scripts can be found in this notebook.

## Analysis.ipynb
Deploying the parsers and generating datasets is done here. This is the bear bones of the notebook given the early stage of the parser functionality. Once parsing is in a more fixed state it will likely be streamlined with high-level APIs to perform the bulk of the functionality across the entire database. This notebook will then be dedicated to extracting insight from the parsed recipes.

# Planned Work
- Better support for setting up the initial MongoDB
- Robust ingredient parsing using a combination of existing libraries and NLP algorithms
- Instruction Parsing
- analysis.py with streamlined dataset and visualization setups to get insights faster
- Expansion of food blogs scraped
- Large list of potential sources so the libraries could automatically obtain recipes from hundreds of domains and websites
- Efficiency increase for recursive page scrapes
