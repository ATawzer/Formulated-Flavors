import pandas as pd
from recipe_scrapers import scrape_me
import time
import random

#=======================
# Obtaining URLS
#=======================

def add_urls(starting, output='recipe_url_database.csv'):
    
    # File to store urls
    df = pd.read_csv(output)
    
    


#=======================
# Scraper Functions
#=======================

def scrape_database(path='recipe_url_database.csv', output='scraped_database.csv'):
    
    # read in database 
    df = pd.read_csv(path)
    df_scrape = df[df.Read == 0]
    
    # Dictionary to store information
    d1 = {}
    
    # scrape and save information
    for index in df_scrape.index:
        
        # Random Timing
        x = random.randrange(2, 31, 1)
        print(f"Waiting for {x} Seconds.", end='\r')
        time.sleep(x)
        
        # Inits
        d2 = {}
        url = df_scrape.loc[index, 'URL']
        scraper = scrape_me(url)
        
        # save information
        d2['url'] = url
        d2['title'] = scraper.title()
        d2['total_time'] = scraper.total_time()
        d2['yields'] = scraper.yields()
        d2['ingredients'] = scraper.ingredients()
        d2['instructions'] = scraper.instructions()
        d2['rating'] = scraper.ratings()
        d2['id'] = url.split('recipe/')[1].split('/')[0]

        # save
        d1[url] = d2
        df.loc[index, 'Read'] = 1
    
    df.to_csv(path, index=False)
    return d1