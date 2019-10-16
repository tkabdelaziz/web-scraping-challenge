from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    #first url to be scraped with Beautiful Soup and Splinter
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Scrape News title
    news_title = soup.find("div",class_="content_title").text
    #Scarpe News paragraph
    news_p = soup.find("div",class_="article_teaser_body").text

    #--------

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Get feature img url
    base_url = "https://www.jpl.nasa.gov"
    feature_url = base_url + soup.find('footer').find('a',class_="button fancybox")["data-fancybox-href"]

    #---------

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Current Weather
    mars_weather = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #-----------

    #Hemisphere Data
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    results = soup.find_all('div', class_='item')
    hemisphere_img_urls = []
    for result in results:
        title = result.find('h3').text
        img_href = result.find('a')['href']
        base_url = "https://astrogeology.usgs.gov/"
        #click link to image
        browser.visit(base_url+img_href)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        #grab img url
        img_url = downloads.find("a")["href"]
    
        img ={
            'title':title,
            'img_url':img_url
        }
        hemisphere_img_urls.append(img)
    

    # Mars Facts Table
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    df = tables[1]
    df.columns = ['Description','Values']
    df = df.set_index('Description')
    mars_fact_html = df.to_html(index='False')


    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "feature_img": feature_url,
        'mars_weather': mars_weather,
        'mars_facts': mars_fact_html,
        'hemisphere_urls':hemisphere_img_urls

    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data