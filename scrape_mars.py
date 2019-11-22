# Scrape Web Data about Mars and Return one Library to collect all the scrape data
# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import time


# Define scrape function
def scrape():
    # Create a library that holds all the Mars' Data
    mars_library = {}
    # Execute Chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    # NASA Mars News
    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)
    soup1 = bs(browser.html, "html.parser")
    slide_elem=soup1.select_one("ul.item_list li.slide")
    news_title=slide_elem.find(class_="content_title").get_text()
    news_p=slide_elem.find(class_="article_teaser_body").get_text()
    # put infos into Library
    mars_library['news_title'] = news_title
    mars_library['news_p'] = news_p


    # JPL Mars Space Images - Featured Image
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
    soup2 = bs(browser.html, "html.parser")
    partial_address = soup2.find_all(class_='fancybox')[0].get('data-fancybox-href').strip()
    featured_image_url = "https://www.jpl.nasa.gov"+partial_address
    mars_library['featured_image_url'] = featured_image_url

    # Mars Weather
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    soup3 = bs(browser.html, "html.parser")
    #scrap latest Mars weather tweet
    mars_weather = soup3.find_all(class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text
    # Put infos into Library
    mars_library['mars_weather'] = mars_weather

    # Mars Facts
    url4 = 'https://space-facts.com/mars/'
    tables = pd.read_html(url4)
    df = tables[0]
    df.columns=['description','value']
    df.set_index('description', inplace=True)
    mars_facts=df.to_html(justify='left')
    mars_library['mars_facts'] = mars_facts

    # Mars Hemisperes
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)
    soup5 = bs(browser.html,"html.parser")
    hemisphere_image_urls = []
    dict = {}
    results = soup5.find_all('h3')
    for result in results:
        itema = result.text
        time.sleep(1)    
        browser.click_link_by_partial_text(itema)
        time.sleep(1)
        soupa = bs(browser.html,"html.parser")
        time.sleep(1)
        linka = soupa.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
        time.sleep(1)
        dict["title"]=itema
        dict["img_url"]=linka 
        hemisphere_image_urls.append(dict)
        dict = {}
        browser.back()
        time.sleep(1)
    # Put infos into Library
    mars_library['hemisphere_image_urls']=hemisphere_image_urls
    
    # Return Library
    return mars_library

