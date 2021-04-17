# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 21:18:53 2021

@author: Viji
"""

from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    url = "https://redplanetscience.com/"
    browser.visit(url)
    time.sleep(1)
    
    news_html = browser.html
    news_soup = bs(news_html,'lxml')
    
    news_title = news_soup.find_all('div', class_='content_title')[0].text.strip()
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text.strip()
    news_title
    news_p

    img_url = 'https://spaceimages-mars.com/'
    browser.visit(img_url)
    time.sleep(1)
    
    img_html = browser.html
    img_soup = bs(img_html,'lxml')
    
    featured_image_path = img_soup.find_all('img', class_='headerimage fade-in')[0]
    featured_image_url = img_url + featured_image_path
    featured_image_url
    
    facts_url = 'https://galaxyfacts-mars.com/'
    browser.visit(facts_url)
    time.sleep(1)
    
    mars_facts = pd.read_html("https://galaxyfacts-mars.com/")[0]
    mars_facts.reset_index(inplace=True)
    mars_facts.columns=["ID", "Properties", "Mars", "Earth"]
    mars_facts
    
    
    # Quit the browser
    browser.quit()

