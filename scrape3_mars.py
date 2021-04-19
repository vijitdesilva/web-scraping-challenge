# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 00:06:26 2021

@author: Viji
"""

# Dependencies and Setup
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import datetime as dt
#Site Navigation
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# # Mars News Web Scraper

def mars_news(browser):
    # Visit the NASA Mars News Site
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url )
    news_html = browser.html
    news_soup = bs(news_html,'lxml')
    
    news_title = news_soup.find_all('div', class_='content_title')[0].text.strip()
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text.strip()
    return news_title, news_p

def featured_image(browser):
    img_url = 'https://spaceimages-mars.com/'
    img_html = browser.html
    img_soup = bs(img_html,'lxml')
    featured_image_path = img_soup.find_all('img', class_='headerimage fade-in')[0]["src"]
    featured_image_url = img_url + featured_image_path
    return featured_image_url

def mars_facts():
    facts_url = 'https://galaxyfacts-mars.com/'
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[0]
    mars_facts.reset_index(inplace=True)
    mars_facts.columns=["Properties", "Mars", "Earth"]
    return mars_facts

def hemisphere(browser):
    hemisphere_url = 'https://marshemispheres.com/'
    browser.visit(hemisphere_url)
    hemisphere_html = browser.html
    hemisphere_soup = bs(hemisphere_html,'lxml')
    hemisphere_names = []

# Search for the names of all four hemispheres
    results = hemisphere_soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

# Get text and store in list
    for name in hemispheres:
        hemisphere_names.append(name.text)
        hemisphere_names
        
    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []

    for thumbnail in thumbnail_results:
    
    # If the thumbnail element has an image...
        if (thumbnail.img):
        
        # then grab the attached link
            thumbnail_url = 'https://marshemispheres.com/' + thumbnail['href']      
        # Append list with links
        thumbnail_links.append(thumbnail_url)
        return thumbnail_links

    full_imgs = []
    for url in thumbnail_links:
    
    # Click through each thumbanil link
        browser.visit(url)
    
        html = browser.html
        soup = bs(html, 'html.parser')
    
    # Scrape each page for the relative image path
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
    
    # Combine the reltaive image path to get the full url
        img_link = 'https://astrogeology.usgs.gov/' + relative_img_path
    
    # Add full image links to a list
        full_imgs.append(img_link)
        return full_imgs
    # Zip together the list of hemisphere names and hemisphere image links
    mars_hemi_zip = zip(hemisphere_names, full_imgs)

    hemisphere_image_urls = []

# Iterate through the zipped object
    for title, img in mars_hemi_zip:
    
        hemisphere_dict = {}
    # Add hemisphere title to dictionary
        hemisphere_dict['title'] = title
    
    # Add image url to dictionary
        hemisphere_dict['img_url'] = img
    
    # Append the list with dictionaries
        hemisphere_image_urls.append(hemisphere_dict)

        return hemisphere_image_urls

def scrape3(browser):
  # Store data in a dictionary
    mars_data = {
        "mars_news": mars_news,
        "featured_image": featured_image,
        "mars_facts": mars_facts,
        "hemisphere": hemisphere
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data