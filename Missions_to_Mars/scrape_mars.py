# Dependencies
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import pandas as pd
import time
import os

if os.name=="nt":
    executable_path = {'executable_path': './chromedriver.exe'}
else:
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

browser = Browser('chrome', **executable_path, headless=False)

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    import os
    if os.name=="nt":
        executable_path = {'executable_path': './chromedriver.exe'}
    else:
        executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)
    time.sleep(5)

def nasa_mars_news():
    browser = init_browser()
    nasa_url = 'https://mars.nasa.gov/news'
    browser.visit(nasa_url)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    nasa_news  = []
    for slides in soup.find_all('li', class_='slide'):
        news_title = slides.find_all('div', class_='content_title')[0].text
        news_p = slides.find_all('div', class_='article_teaser_body')[0].text
        print(f"News_Title:{news_title}")
        print(f"News_Paragraph:{news_p}")
        nasa_news.append({"News_Title" : news_title, "News_Paragraph" : news_p})
        break
    browser.quit()
    return nasa_news

def featured_mars_img():
    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(5)
    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'lxml')
    image_url = soup.find('article', class_='carousel_item')['style']
    mars_image_url =image_url.replace('background-image: url(', '').replace(');','')[1:-1]
    main_url = 'https://www.jpl.nasa.gov'
    featured_image_url = main_url + mars_image_url
    browser.quit()
    return featured_image_url 
featured_mars_img()

def mars_weather_twitter():
    browser = init_browser()
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')
    mars_weather = soup.find_all('span')
    for tweet in mars_weather:
        if 'InSight sol' in tweet.text:
            mars_weather = tweet.text
        break
    browser.quit()
    return mars_weather

mars_weather_twitter()

twitter_url ='https://twitter.com/marswxreport?lang=en'

browser.visit(twitter_url)
time.sleep(5)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')


mars_weather = soup.find_all('span')
for tweet in mars_weather:
    if 'InSight sol' in tweet.text:
        mars_weather = tweet.text
        print(f"Mars Weather:{mars_weather}")
        break


facts_url = 'https://space-facts.com/mars/'

tables = pd.read_html(facts_url)
tables

type(tables)

df = tables[0]
df.columns = ['Mars_Profile','Facts']

html_table = df.to_html()
html_table

images_url ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


browser.visit(images_url)
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

results = soup.find_all('div', class_='item')
print(results)

# Loop through returned results
hem_title_urls  = []
main_url = 'https://astrogeology.usgs.gov'


for result in results:
    title = result.find('h3').text
    image_url = result.find('a', class_='itemLink product-item')['href']
    image_url = main_url+image_url
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    result = browser.links.find_by_text('Sample').first
    enhansed_url = result['href']
    hem_title_urls.append({"Title" : title, "Image_URL" : enhansed_url})   

hem_title_urls

# get_ipython().system('jupyter nbconvert --to script mission_to_mars.ipynb')