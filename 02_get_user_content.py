# > pip install jsonlines

import os
import requests
import jsonlines
import csv
from dotenv import load_dotenv
import bs4 as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import TimeoutExceptionfrom
from selectorlib import Extractor
import time


# helpers
# from https://gist.github.com/dariodiaz/3104601
def highlight(element):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent

    def apply_style(s):
        driver.execute_script(
            "arguments[0].setAttribute('style', arguments[1]);", element, s)
    original_style = element.get_attribute('style')
    apply_style("background: yellow; border: 2px solid red;")
    time.sleep(.3)
    apply_style(original_style)


# pull passwords
load_dotenv() 
LOGIN = os.getenv('LOGIN')
LOGINP = os.getenv('LOGINP')


# log in via selenium.  
#  leaves 10 seconds to manually click log in and maybe solve captcha, etc
driver = webdriver.Chrome(ChromeDriverManager().install())
if True:
    url = "https://www.worldpulse.com/my-pulse/voices"
    driver.get(url)
    driver.implicitly_wait(10)  # seconds
    element = driver.find_element(By.CSS_SELECTOR, 'input#edit-name')
    element.send_keys('enfascination')
    element = driver.find_element(By.ID, 'edit-pass')
    element.send_keys(LOGINP)
    time.sleep(5)
    #  driver.find_element(By.ID, 'edit-submit').click()


# scroll through pages of user posts to extract user urls for later scraping
users = []
with open('user_list.csv', 'r') as fp:
    dict_reader = csv.DictReader(fp)
    for d in dict_reader:
        user = dict(d)
        users.append(user)

with jsonlines.open('user_info.jsonl', 'w') as writer:
    for i, user in enumerate(users):
        # for debugging
        if i > 2:
            break
        url = "https://www.worldpulse.com" + user['url']
        print(i, url)
        # boilerplate
        driver.get(url)
        driver.implicitly_wait(10)  # seconds
        soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
        # scrape key info
        user['id'] = int(soup.find('worldpulse-impact')['data-user'])
        user['has_initiative'] = None
        user['has_bio'] = None
        user['has_posts'] = None
        user['has_activity'] = None
        badgeEls = soup.find_all('div', class_='badge-item')
        user['badges'] = [el.find('img')['title'] for el in badgeEls]
        user['date_joined'] = None
        user['followers'] = None
        user['following'] = None
        user['impact_total'] = None
        user['initiatives'] = None
        user['initiative_updates'] = None
        user['impact_goal'] = None
        user['impact_time'] = None
        user['tags'] = None
        user['posts_count'] = None
        user['posts'] = None
        activity_head = soup.find('h1', string='Activity')
        activity_list = activity_head.next_sibling.find_all('a', class_='list-group-item') 
        activity_list_clean = [{'activity': a.text, 'url': a['href']} for a in activity_list]
        user['activity_count'] = len(activity_list)
        user['activity'] = activity_list_clean
        user['about'] = ''''''
        writer.write(user)



