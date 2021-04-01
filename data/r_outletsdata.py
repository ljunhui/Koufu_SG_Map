# %% Import
import numpy as np
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup

""" 
Takes a dictionary of relevant brands and their URLs and returns a raw csv file
"""
# %% Functions


def outlets_crawl(brand, url):
    """
    Returns a raw, unformatted df of outlets with it's brand from the url inserted
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "lxml")

    # ensure crawler had actual results to work with.
    def _check_results(class_term, soup=soup):
        results = soup.find_all(attrs={"class": class_term})
        if len(results) == 0:
            raise ValueError("No outlets found, check class_term or url.")
        return results

    try:
        results = _check_results("outlet_item")
    except ValueError:
        results = _check_results("lease_item")

    # continue
    _ls = []
    for result in results:
        _ls.append([i for i in result.stripped_strings])

    df = pd.DataFrame(_ls)
    df.insert(0, "brand", brand, allow_duplicates=True)
    return df


def loop_outlets_crawl(dict, outputfn):
    """
    Loops outlets_crawl func through a dictionary of urls and their brands. Returns a concatenated df and saves it as a temporary csv.
    """
    _ls = []
    for brand, url in dict.items():
        _ls.append(outlets_crawl(brand, url))
        print(f"{brand} done.")
    df = pd.concat(_ls)
    df.to_csv(outputfn, index=False)


def main():
    url_dict = {
        "Koufu": "https://www.koufu.com.sg/our-brands/food-halls/koufu/",
        "Cookhouse": "https://www.koufu.com.sg/our-brands/food-halls/cookhouse/",
        "Rasapura": "https://www.koufu.com.sg/our-brands/food-halls/rasapura-masters/",
        "ForkSpoon": "https://www.koufu.com.sg/our-brands/food-halls/fork-spoon/",
        "HappyHawkers": "https://www.koufu.com.sg/our-brands/food-halls/happy-hawkers/",
        "Gourmet": "https://www.koufu.com.sg/our-brands/food-halls/gourmet-paradise/",
        "R&B": "https://www.koufu.com.sg/our-brands/concept-stores/rb-tea/",
        "1983NY": "https://www.koufu.com.sg/our-brands/concept-stores/1983-a-taste-of-nanyang/",
        "Supertea": "https://www.koufu.com.sg/our-brands/concept-stores/supertea/",
        "1983CT": "https://www.koufu.com.sg/our-brands/cafe-restaurants/1983-coffee-toast/",
        "Elemen": "https://www.koufu.com.sg/our-brands/cafe-restaurants/elemen-%e5%85%83%e7%b4%a0/",
        "Grove": "https://www.koufu.com.sg/our-brands/cafe-restaurants/grovecafe/",
    }

    outputfn = "./r_outletsdata.csv"
    if os.path.isfile(outputfn):
        os.remove(outputfn)
    loop_outlets_crawl(url_dict, outputfn)


# %% Main
if __name__ == "__main__":
    main()
    os.system("pause")
