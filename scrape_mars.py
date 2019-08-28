# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():
    browser = init_browser()

    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    time.sleep(5)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = bs(html, 'html.parser')

    # Examine the results, then determine element that contains the latest News Title
    news_title = soup.find('div', class_="content_title").text.strip()
    # print(news_title)

    # Examine the results, then determine element that contains the related Paragraph Text
    news_p = soup.find('div', class_="article_teaser_body").text.strip()
    # print(news_p)

    # Create variables for webpaths (1 for base and 2 for relative)
    url_1='https://www.jpl.nasa.gov'
    url_2='/spaceimages/?search=&category=Mars'

    # URL of page to be scraped for image
    url_pic= url_1 + url_2
    # url_pic = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_pic)

    time.sleep(5)

    # Go to next page that has full image
    browser.click_link_by_partial_text("FULL IMAGE")

    html_image= browser.html
    soup_image = bs(html_image, 'html.parser')

    time.sleep(5)

    # Examine the results, then determine element that contains the related featured image 
    featured_image_container=soup_image.find('div', class_="fancybox-inner")

    time.sleep(5)

    featured_image_img = None
    featured_image_path = featured_image_container.find_all('img', class_="fancybox-image")
    if len(featured_image_path):
        featured_image_path = featured_image_path[0]['src']
        featured_image_img = url_1 + featured_image_path
    else:
        featured_image_path = "https://www.jpl.nasa.gov/images/mars2020/20190726/PIA23212-16.jpg"
        featured_image_img = featured_image_path
    #   featured_image_path = featured_image_container.find_all('img', class_="fancybox-image")[0]["src"]



    time.sleep(5)

    # Twitter account to be scraped
    url_twit = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_twit)

    # Create BeautifulSoup object; parse with 'html.parser'
    html_twit = browser.html
    soup_twit = bs(html_twit, 'html.parser')

    # Examine the Twitter results, determine element that contains the related Paragraph Text
    mars_weather = soup_twit.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text.strip()
    # print(mars_weather)

    # URL of page to be scraped
    url_mars = 'https://space-facts.com/mars/'
    browser.visit(url_mars)

    # use the read_html function to automatically scrape any tabular data from page.
    tables = pd.read_html(url_mars)

    #Remove extra table, only want table 1, create df
    df = tables[1]

    #Rename columns
    df.columns=["description","value"]

    mars_facts = df.to_html()
    # mars_facts

    # Create variables for URL of page to be scraped for image of hemispheres
    url_hemi_1 ='https://astrogeology.usgs.gov'
    url_hemi_2 ='/search/results?q=hemisphere+enhanced&amp;k1=target&amp;v1=Mars'
    url_hemis = url_hemi_1 + url_hemi_2
    browser.visit(url_hemis)


    # Go to next page that has full image
    browser.click_link_by_partial_text("Cerberus")

    html_image_cer= browser.html
    soup_image_2 = bs(html_image_cer, 'html.parser')


    cerberus_image=soup_image_2.find('img', class_="wide-image")["src"]
    cerberus_image_img = url_hemi_1 + cerberus_image

    # Go to next page that has full image
    browser.click_link_by_partial_text("Schiaparelli")

    html_image_sch= browser.html
    soup_image_3 = bs(html_image_sch, 'html.parser')

    schiaparelli_image=soup_image_3.find('img', class_="wide-image")["src"]
    schiaparelli_image_img = url_hemi_1 + schiaparelli_image
    print(schiaparelli_image_img)

    # Go to next page that has full image
    browser.click_link_by_partial_text("Syrtis")

    html_image_syrtis= browser.html
    soup_image_4 = bs(html_image_syrtis, 'html.parser')
    syrtis_image=soup_image_4.find('img', class_="wide-image")["src"]
    syrtis_image_img = url_hemi_1 + syrtis_image

    # Go to next page that has full image
    browser.click_link_by_partial_text("Valles")

    html_image_valles= browser.html
    soup_image_5 = bs(html_image_valles, 'html.parser')
    valles_image=soup_image_5.find('img', class_="wide-image")["src"]
    valles_image_img = url_hemi_1 + valles_image
    print(valles_image_img)

    # Store data in a dictionary
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere", "img_url": "cerberus_image_img"},
        {"title": "Schiaparelli Hemisphere", "img_url": "schiaparelli_image_img"},
        {"title": "Syrtis Major Hemisphere", "img_url": "syrtis_image_img"},
        {"title": "Valles Marineris Hemisphere", "img_url": "valles_image_img"}
    ]

   #Store all data in a dictionary
    mars_data= {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_img": featured_image_img,
        "mars_weather": mars_weather,
        "mars_facts": mars_facts,
        "title1": "Cerberus Hemisphere Enhanced", 
        "cerberus_image_img": cerberus_image_img,
        "title2": "Schiaparelli Hemisphere Enhanced", 
        "schiaparelli_image_img": schiaparelli_image_img,
        "title3": "Syrtis Major Hemisphere Enhanced", 
        "syrtis_image_img": syrtis_image_img,
        "title4": "Valles Marineris Hemisphere Enhanced", 
        "valles_image_img": valles_image_img,
    }

    # Close the browser after scraping
    browser.quit()      

    # Return results
    return mars_data