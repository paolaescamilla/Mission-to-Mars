# Import Splinter and BeautifulSoup and pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt


def scrape_all():
    #initiate headless driver for deployment
    executable_path={'executable_path':ChromeDriverManager().install()}
    browser=Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph=mars_news(browser)

    #run all scrapping functions and store results in dictionary
    data={
        'news_title':news_title,
        'news_paragraph': news_paragraph,
        'featured_image':featured_image(browser),
        'facts': mars_facts(),
        'last_modified':dt.datetime.now(),
        'hemisphere_dict': hemispheres(browser)
    }

    #stop webdriver and return data
    browser.quit()
    return data
    
    

def mars_news(browser):

    #scrape mars news
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object and then quit the browse
    html = browser.html
    news_soup = soup(html, 'html.parser')

    #Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None


    return news_title, news_p

# ### JPL Space Imagees Featured image

# declare and define our function
def featured_image(browser):

    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    #add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None


    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'


    return img_url

# ## Mars Facts
#define our function
def mars_facts():

    try:
        #use read_html to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    #Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    #convert dataframe into HTML format, add bootstrap
    return df.to_html(classes='table table-striped')

def hemispheres(browser):
    hemisphere_dict = {}

    url = 'https://marshemispheres.com/'

    browser.visit(url)

    browser.is_element_present_by_css('div.list_text', wait_time=1)

    for i in range (4):
        titles=browser.find_by_css('h3')
        titles[i].click()
        html=browser.html
        soup=BeautifulSoup(html, 'html.parser')
        url=soup.find('img', class_='wide-image')['src']
        tile=soup.find('h2', class_='title').txt
        image_url = 'https://astrogeology.usgs.gov'+ url
        image_dict = {"title":titles,"image_url":url}
        hemisphere_image_urls.append('image_dict')
        browser.back()

    return hemisphere_dict

if __name__ == '__main__':
    # if running as script, print scraped data
    print(scrape_all())




