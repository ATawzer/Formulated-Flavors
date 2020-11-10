# Formulated Flavors
The code and analysis tools behind the website formulatedflavors.com, a food blog exploring data-driven recipe creation and perfection. Using a collection of web scrapers, nearly 250,000 recipes have been pulled from the best recipe sites and food blogs from across the internet. By analyzing staple foods, like a chocolate chip cookie, across so many recipe creators the hope is to find the optimal recipe. Formulated Flavors, then, is the data-backed compression of an internet’s worth of recipes into a small set of well-designed recipes.

The code in this repository focuses on 3 functions: Scraping, Parsing and Analyzing. Scraping offers quick functions that allow for mass recipe gathering with very little knowledge of the recipe sites and minimal work upfront for the user. Parsing allows for the processing of the recipes into more machine-readable formats. Analysis employs the newly acquired and structured data to find the best ways to make or improve a recipe.

# Scraping - Building a Recipe Database
There are two major sources of recipes: recipe sites and food blogs. Sites like AllRecipes.com or Food.com are good examples of a recipe site. They contain large amounts of recipes submitted by a large user base. Food blogs on the other hand are typically a single author creating many recipes and provide more information (pictures, anecdotes, etc.) around the recipes. While it was attempting to let the bulk of the recipes come from a single few sources and recipe sites for technical simplicity, it was important that food blogs were well represented. Food blogs have many of the high-quality and well-crafted recipes that circulate through Pintrest and Yummly. To ensure that the optimal recipe exists as the aggregate of the recipes in the database it was important to have the perfect mix recipe types.

## scrapers.py
There are two methods in the scraping methodology. One was to leverage an existing recipe scraping package (see the requirements section) with pre-built hooks into some of the most popular recipe sites and a few well-known food blogs. The second is a food-blog agnostic approach which leverages a popular WordPress recipe format that a large chunk of food blogs use now or have switched to using recently. While paging through a food blog is slower, it is extremely easy to setup and allows the seamless integration of many different sources.

RecipeCollector: A web-crawler object for recursively scraping an entire food blogs catalog of recipes. All that is needed to spin a crawler up is the starting page and some DB tagging. This works by recursively exploring every link on a website and tracking which pages have been visited. If the crawler comes across a page where it finds the wordpress recipe format, it will scrape it. This makes it very clean to get a consistent data feed from each food blog and get a full set of recipes without having to specify the individual food blog’s page structure.

## db_funcs.py

# Parsing – Machine readable Recipes

## parsers.py

# Analysis
The ultimate output are clean analysis ready datasets for staple foods. There are many challenges to getting to this point, most of which fall in the realm of NLP. Some of the challenges are listed below:

Ingredients – Since the source is mostly food blogs, ingredients

For a more tangible view of the output see the choco_chip_worksheet.xlsx. This contains a manually assembled recipe comparison to show where certain recipes succeed and fall short.

# Future Progress
