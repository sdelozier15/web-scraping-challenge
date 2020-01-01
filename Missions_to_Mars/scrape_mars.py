#Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

# one scrape to rule them all...
def scrape():
    print("Scraping Mars")
    news = scrape_news()
    images = scrape_images()
    weather = scrape_weather()
    facts = scrape_facts()
    hemispheres = scrape_hemispheres()
    
    results = {
        'news':news, \
        'images':images, \
        'weather':weather, \
        'facts':facts, \
        'hemispheres':hemispheres \
    }

    print(results)
    
    return results

# scraping functions (from Jupyter notebook)
def scrape_news():
    #NASA Mars News

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome')

    url1 = 'https://mars.nasa.gov/news/'
    browser.visit(url1)

    html = browser.html
    soup = bs(html, 'html.parser')

    article = soup.find('div', class_='image_and_description_container')

    title = article.h3.text
    summary = article.div.text

    browser.quit()

    return [title, summary, url1]

def scrape_images():
    #JPL Mars Space Images - Featured Image

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome')

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    browser.visit(url2)

    url_string = "https://www.jpl.nasa.gov"
    html = browser.html
    soup = bs(html, 'html.parser')

    featured = soup.find('div', class_='carousel_items')

    image_url = featured.a.get('data-fancybox-href')
    data_url = featured.a.get('data-link')
    image_link = f'{url_string}{image_url}'
    data_link = f'{url_string}{data_url}'
    description = featured.article.get('alt')

    browser.quit()

    return [image_link, data_link, description]

def scrape_weather():
    #Mars Weather

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome')

    url3 = "https://twitter.com/marswxreport?lang=en"

    browser.visit(url3)

    html = browser.html
    soup = bs(html, 'html.parser')

    tweet = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    mars_weather = tweet.contents[0]
    tweet_link = tweet.contents[1].get('href')

    browser.quit()

    return [mars_weather, tweet_link]

def scrape_facts():
    #Mars Facts

    url4 = "https://space-facts.com/mars/"

    tables = pd.read_html(url4)

    mars_earth = pd.DataFrame(tables[0])

    mars_facts = pd.DataFrame(tables[1])

    table = mars_facts.to_html()

    return table

def scrape_hemispheres():
    #Mars Hemispheres

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome')

    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    url_text = "https://astrogeology.usgs.gov"

    browser.visit(url5)
    time.sleep(1)

    html = browser.html
    soup = bs(html, 'html.parser')

    hemispheres = soup.find_all('div', class_='item')

    titles = []
    urls = []

    for item in hemispheres:
        title = item.h3.text
        title = title.replace(' Enhanced', '')
        titles.append(title)
        
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        html = browser.html
        soup = bs(html, 'html.parser')

        image = soup.find('img', class_='wide-image')
        link = image.get('src')
        urls.append(f'{url_text}{link}')
        
        browser.visit(url5)
        time.sleep(1)

    browser.quit()

    hemisphere_urls = [{"title":titles[0],"url_img":urls[0]},\
            {"title":titles[1],"url_img":urls[1]},\
            {"title":titles[2],"url_img":urls[2]},\
            {"title":titles[3],"url_img":urls[3]},]

    return hemisphere_urls
