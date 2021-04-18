# -*- coding: utf-8 -*-
"""
Created on Sat Apr 17 18:18:53 2021

@author: Viji
"""
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
#Site Navigation
executable_path = {"executable_path": "/Users/sharonsu/Downloads/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)


# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = marsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = marsImage()
    final_data["mars_facts"] = marsFacts()
    final_data["mars_hemisphere"] = marsHem()

    return final_data

# # NASA Mars News

def marsNews():
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    news_html = browser.html
    soup = bs(news_html, "lxml")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

# # JPL Mars Space Images - Featured Image
def marsImage():
    img_url = "https://spaceimages-mars.com/"
    browser.visit(img_url)
    img_html = browser.html
    soup = bs(img_html, "lxml")
    featured_image_path = soup.find("img", class_="thumb")["src"]
    featured_img_url = img_url + featured_image_path
    return featured_img_url


# # Mars Facts
def marsFacts():
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    mars_facts = pd.read_html(facts_url)
    mars_facts = pd.DataFrame(mars_facts[0])
    mars_facts.columns = ["ID", "Properties", "Mars", "Earth"]
    mars_facts = mars_facts.set_index("ID")
    mars_facts = mars_facts.to_html(index = True, header =True)
    return mars_facts


# # Mars Hemispheres
def marsHem():
    hemisphere_url = "https://marshemispheres.com/"
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html,'lxml')
    hemisphere_names = []

    products = hemisphere_soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "lxml")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        hemisphere_names.append(dictionary)
    return hemisphere_names