# coding: utf-8

#Imports & Dependencies
from splinter import Browser
from bs4 import BeautifulSoup

#Site Navigation
executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
browser = Browser("chrome", **executable_path, headless=False)

##News

def marsNews():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text
    output = [news_title, news_p]
    return output

##Images
def marsImage():
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    return featured_image_url

## Weather
def marsWeather():
    
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    tweet = soup.find("div", class_='stream')
    mars_twitter = tweet.find("div", class_ ="js-tweet-text-container").text
    return mars_twitter

# # Mars Facts
def marsFacts():
    import pandas as pd
    marsfx_url = "https://space-facts.com/mars/"
    browser.visit(marsfx_url)
    mars_data = pd.read_html(marsfx_url)
    mars_data = pd.DataFrame(mars_data[0])
    mars_data.columns = ["Mars_Description", "Value"]
    mars_data = mars_data.set_index("Description")
    mars_facts = mars_data.to_html(index = True, header =True)
    return mars_facts


# # Mars Hemispheres
def marsHem():
    import time 
    mhemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(mhemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        dictionary = {"title": title, "img_url": image_url}
        mars_hemisphere.append(dictionary)
    return mars_hemisphere

# Main scrape function
def scrape():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    mars_results = {}
    output = marsNews()
    mars_results["mars_news"] = output[0]
    mars_results["mars_text"] = output[1]
    mars_results["mars_image"] = marsImage()
    mars_results["mars_weather"] = marsWeather()
    mars_results["mars_facts"] = marsFacts()
    mars_results["mars_hemisphere"] = marsHem()
   
    # mars_news = output(browser)
    # img_url = featured_image_url(browser)
    # mars_weather = mars_twitter(browser)
    # facts = mars_facts()
    # hemisphere_images = mars_hemisphere(browser)

    # mars_results = {
    #     #"news_title": news_title,
    #     #"news_paragraph": news_paragraph,
    #     "featured_image": img_url,
    #     "weather": mars_weather,
    #     "facts": facts,
    #     "hemispheres": hemisphere_images,
    # }
    browser.quit()
    return mars_results

if __name__ == "__main__":
    print(scrape())