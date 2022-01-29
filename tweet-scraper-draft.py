import pandas as pd
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from numpy import NaN

# print("Enter the month in number (e.g. 01, 02, etc)!")
# bulan = input('= ')
bulan = '12'
keyword = 'indonesia'

options = webdriver.ChromeOptions()
options.add_argument(r'--user-data-dir=C:\Users\Saidzzz\AppData\Local\Google\Chrome\User Data\Default')
options.add_argument('--profile-directory=Default')
options.headless = True # To make browser disappear

s = Service(r"D:/physics/python/chromedriver.exe")
url = f"https://twitter.com/search?q=({keyword})%20until%3A2021-{int(bulan) + 1}-01%20since%3A2021-{bulan}-01&src=typed_query&f=live"

driver = webdriver.Chrome(service=s, options=options)
driver.get(url)

wait = WebDriverWait(driver, 10)
time.sleep(3)

# xpath other than tweet are relative to the tweet xpath
xpath = {
    'tweet': '//article[@data-testid="tweet"]',
    'name': './div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[1]/div[1]/span/span',
    'username': './div/div/div/div[2]/div[2]/div[1]/div/div/div[1]/div[1]/a/div/div[2]/div/span',
    'date': './/time',
    'reply_to': './div/div/div/div[2]/div[2]/div[2]/div[1]/div/div/a/span',
    'content': './div/div/div/div[2]/div[2]/div[2]/div[@class="css-1dbjc4n"]',
    'reply': './/div[@data-testid="reply"]/div/div[2]',
    'retweet': './/div[@data-testid="retweet"]/div/div[2]',
    'like': './/div[@data-testid="like"]/div/div[2]'
}

try:
    wait.until(ec.presence_of_element_located(
        (By.XPATH, xpath['tweet'])))
except NoSuchElementException:
    print("No element ternyata")
    driver.close()
print("We've entered")

data = ['Test (delete this)']

# To check if the tweet is the last one, the upper bound is 120
none_count = 0

try:
    wait.until(
        ec.presence_of_element_located((By.XPATH, xpath['tweet'])),
        message="No element article"
    )
    time.sleep(1)
    tweets = driver.find_elements(By.XPATH, xpath['tweet'])
    i = 2

    name = tweets[i].find_element(By.XPATH, xpath['name']).text
    username = tweets[i].find_element(By.XPATH, xpath['username']).text

    # there are advertisment tweets without date
    try:
        date = tweets[i].find_element(By.XPATH, xpath['date']).text
    except NoSuchElementException:
        date = NaN

    # there are tweets with reply_to elements, but not all
    try:
        reply_to = tweets[i].find_element(By.XPATH, xpath['reply_to']).text
    except NoSuchElementException:
        reply_to = NaN

    content = tweets[i].find_element(By.XPATH, xpath['content']).text
    reply = tweets[i].find_element(By.XPATH, xpath['reply']).text
    retweet = tweets[i].find_element(By.XPATH, xpath['retweet']).text
    like = tweets[i].find_element(By.XPATH, xpath['like']).text
    id = ''.join([name.replace(' ', ''), str(date).replace(' ', '').replace(',', ''), content[:3] if bool(content) else ''])
    print(f'id: {id}')
    print(f'{name} | {username} | {date}')
    print(f'Replying to: {reply_to}')
    print(f'{content}')
    print(f'Number of reply: {int(reply) if bool(reply) == True else 0}')
    print(f'Number of retweet: {int(retweet) if bool(retweet) == True else 0}')
    print(f'Number of like: {int(like) if bool(like) == True else 0}')

except Exception as wow:
    print(wow)

time.sleep(5)

driver.close()