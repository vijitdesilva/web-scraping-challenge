# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 21:12:51 2021

@author: Viji
"""

from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager


#Site Navigation
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


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

# # Mars News

def marsNews():
    news_url = "https://redplanetscience.com/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

# # JPL Mars Space Images - Featured Image
def marsImage():
    image_url = "https://spaceimages-mars.com/"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="headerimage fade-in")["src"]
    featured_image_url = "https://spaceimages-mars.com/" + image
    return featured_image_url

# # Mars Facts
def marsFacts():
    import pandas as pd
    facts_url = "https://galaxyfacts-mars.com/"
    browser.visit(facts_url)
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Properties", "Mars", "Earth"]
    mars_data = mars_data.set_index("Properties")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts


# # Mars Hemispheres
def marsHem():
    hemispheres_url = 'https://marshemispheres.com/'
    browser.visit(hemispheres_url)
    hemisphere_html = browser.html
    hemisphere_soup = BeautifulSoup(hemisphere_html,'html.parser')
    
    hemisphere_names = []

    results = hemisphere_soup.find_all('div', class_="collapsible results")
    hemispheres = results[0].find_all('h3')

    for name in hemispheres:
        hemisphere_names.append(name.text)
    
    
    thumbnail_results = results[0].find_all('a')
    thumbnail_links = []
    
    for thumbnail in thumbnail_results:
        if (thumbnail.img):
            thumbnail_url = 'https://marshemispheres.com/' + thumbnail['href']
            thumbnail_links.append(thumbnail_url)
    
    full_imgs = []

    for url in thumbnail_links:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        results = soup.find_all('img', class_='wide-image')
        relative_img_path = results[0]['src']
        
        img_link = 'https://marshemispheres.com/' + relative_img_path
        full_imgs.append(img_link)
        
    mars_hemi_zip = zip(hemisphere_names, full_imgs)
    hemisphere_image_urls = []
    
    for title, img in mars_hemi_zip:
        hemisphere_dict = {}
        hemisphere_dict['title'] = title
        hemisphere_dict['img_url'] = img
        hemisphere_image_urls.append(hemisphere_dict)
    return hemisphere_image_urls
            
            
    browser.quit()

if __name__ == '__main__':
    scrape()