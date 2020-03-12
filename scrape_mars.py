    #!/usr/bin/env python
    # coding: utf-8

    # In[1]:


import pandas as pd
import requests
from splinter import Browser
from bs4 import BeautifulSoup as bs
from pprint import pprint


    # In[2]:

def scrape():
    nasa_url = 'https://mars.nasa.gov/news/'
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=True)
    browser.visit(nasa_url)
    pprint(browser.html)
# Set headless=True, it stops opening windows everytime running scrape function

    # In[3]:


    soup = bs(browser.html, 'lxml')
    # print(soup.prettify())


    # In[4]:


    # Collect the latest News Title and Paragraph Text

    result = soup.find('div', class_="image_and_description_container")
    # print(result)
    news_title = result.find('div', class_="content_title").text
    news_p = result.find('div', class_="article_teaser_body").text

    print(news_title)
    print(news_p)


    # In[5]:


    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

    browser.visit(jpl_url)


    # In[6]:


    browser.find_by_css("#full_image").first.click()


    # In[7]:


    browser.links.find_by_partial_text("more info").first.click()


    # In[8]:


    browser.find_by_css(".main_image").first.click()


    # In[9]:


    featured_image_url = browser.url
    print(featured_image_url)


    # In[10]:


    # Scrape the latest Mars weather tweet from the page
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    response=requests.get(weather_url)
    soup = bs(response.text, "lxml")
    # print(soup)
    mars_weather = soup.find_all('p', class_="js-tweet-text")[1].text.split("pic.twitter")[0].split("InSight")[-1]
    print(mars_weather)


    # In[11]:


    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)

    tables


    # In[12]:


    df = tables[0]
    df.set_index(0, inplace=True)
    df = df.rename(columns = {1: "values"})
    del df.index.name
    df


    # In[13]:


    # Use Pandas to convert the data to a HTML table string.
    html_table = df.to_html()
    html_table
    html_table.replace('\n', '')


    # In[14]:


    # Obtain high resolution images for each of Mar's hemispheres.
    usgs_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_img_url=[]
    browser.visit(usgs_url)

    for count in range(4):
        link = browser.links.find_by_partial_text('Hemisphere Enhanced')[count]
        link.click()
        title = browser.find_by_css('.title').first.text
        url = browser.find_by_text('Sample').first['href']
        browser.back()
        hemi_img_url.append({
            'title': title,
            'img_url': url
        })

    for url in hemi_img_url:
        print(url)
    
    return({
        'news_title': news_title,
        'news_p': news_p,
        'featured_image_url':featured_image_url,
        'mars_weather': mars_weather,
        'html_table': html_table,
        'hemi_img_url': hemi_img_url
    })


    # In[ ]:




