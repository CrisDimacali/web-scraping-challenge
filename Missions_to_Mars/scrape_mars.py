from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import pandas as pd
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def news():
    browser = init_browser()
    nasa_url = 'https://mars.nasa.gov/news'
    browser.visit(nasa_url)
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    mars_news  = []
    for x in soup.find_all('li', class_='slide'):
        news_title = x.find_all('div', class_='content_title')[0].text
        news_p = x.find_all('div', class_='article_teaser_body')[0].text
        mars_news =  [news_title, news_p]
        break
    browser.quit()
    return mars_news  

def featured_mars():
    browser = init_browser()
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    image = soup.find('article', class_='carousel_item')['style']
    mars_image =image.replace('background-image: url(', '').replace(');','')[1:-1]
    orig_url = 'https://www.jpl.nasa.gov'
    featured_image_url = orig_url + mars_image
    browser.quit()
    return featured_image_url  

def mars_twitter():
    browser = init_browser()
    twitter= 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    mars_weather = soup.find_all('span')
    for i in mars_weather:
        if 'InSight sol' in i.text:
            mars_weather = i.text
            break
    browser.quit()
    return mars_weather 

def mars_facts_table():
    f_url = 'https://space-facts.com/mars/'
    f_tables = pd.read_html(f_url)
    mars_facts = f_tables[0]
    mars_facts.columns = ["Description", "Value"]
    mars_facts = mars_facts.set_index("Description")
    mars_table = mars_facts.to_html()
    return mars_table

def hemisphere_imgs():
    browser = init_browser()
    h_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(h_url)
    time.sleep(2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find_all('div', class_='item')
    hemisphere_urls  = []
    orig_url = 'https://astrogeology.usgs.gov'  
    for y in results:
        title = y.find('h3').text
        image_url = y.find('a', class_='itemLink product-item')['href']
        image_url2 = orig_url+image_url
        browser.visit(image_url2)
        time.sleep(2)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        y = browser.links.find_by_text('Sample').first
        enhanced_url = y['href']
        hemisphere_urls.append({"Title" : title, "Image_URL" : enhanced_url}) 
    browser.quit()  
    return hemisphere_urls


def scrape_info():
    
    mars_info = {}
    # nasa_news = news()
    # mars_info["title"] = mars_news[0]
    # mars_info["par"] = mars_news[1]
    mars_info["featured_image_url"] = featured_mars()
    mars_info["mars_weather"] = mars_twitter()
    mars_info["mars_table"] = mars_facts_table()
    mars_info["hem_title_urls"] = hemisphere_imgs()

    # Return results
    return mars_info