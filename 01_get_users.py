# > pip install selenium
# > pip install webdriver
# > pip install selectorlib
# > pip install python-dotenv

import os
import requests
import csv
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


# pull passwords
env = os.environ.copy()
LOGIN = str(env['LOGIN'])
LOGINP = str(env['LOGINP'])


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
nPages = 2   # set this higher to get more pages and user names
if True:
    with open('user_list.csv', 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=('name', 'url', 'country'))
        writer.writeheader()
        for i in range(0, nPages):  # to avoid starting at the first page, change 0
            url = f"https://www.worldpulse.com/my-pulse/voices?page=0,{i}"
            driver.get(url)
            driver.implicitly_wait(10)  # seconds
            print(i)
            soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
            # order-1 is a class that all user entries are under, but  some other stuff is under it too
            #  hence if statement below for filtering out values without flags
            soup.find_all('div', class_='order-1')
            usersEl = soup.find_all('div', class_='order-1')
            user = {}
            for u in usersEl:
                if u.find('div', class_='user-flag'):
                    user['name'] = u.text
                    user['url'] = u.find('a')['href']
                    user['country'] = u.find('div', class_='user-flag')['title']
                    writer.writerow(user)


