#? IMPORTS
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import json

import sys


#? HELPER FUNCTIONS
def get_title(html_soup):
    title = html_soup.find("h3", class_="post-title entry-title").get_text()
    return title
    

def get_short_desc(html_soup, paras=0):
    div = html_soup.find("div", class_="post-body entry-content float-container")
    spans = div.find_all("span")

    span_str = ""

    for i in range(0, paras):
        span_str += spans[i].get_text()
        span_str += "\n"

    return span_str

def get_first_image(html_soup):
    try:
        div = html_soup.find("div", class_="post-body entry-content float-container")
        img_url = div.find("img")["src"]
    except:
        img_url = ""
    return img_url

#? FUNCTIONS
def get_all_data(link, no_of_paras=1):
    # Get the Whole Page and convert to BS4 Object
    if link == "":
        main_page = requests.get("https://www.supergamingreport.com")._content
        main_page_soup = BeautifulSoup(main_page, features="html.parser")
        div = main_page_soup.find("h3", class_="post-title entry-title")
        link = div.find("a").get('href')

        with open("storage/articles.json") as f:
            articles_json = json.loads(f.read())

        if link in articles_json["links"]:
            return False
        
        articles_json["links"].append(link)

        with open("storage/articles.json", "w") as f:
            json.dump(articles_json, f)

    article = requests.get(link)._content
    article_soup = BeautifulSoup(article, features="html.parser")

    # Section to get Actual Info
    title = get_title(article_soup)
    desc = get_short_desc(article_soup, no_of_paras)
    image_url = get_first_image(article_soup)

    return title, desc, image_url, link

if __name__ == "__main__":
    response = get_all_data("", 1)
    if response == False:
        print(response)

    title, desc, image_url, link = response