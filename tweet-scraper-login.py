import pandas as pd
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from numpy import NaN

class TweetScraper:
    options = webdriver.ChromeOptions()
    # For remembering the previous login session
    # options.add_argument(r'--user-data-dir=C:\Users\Saidzzz\AppData\Local\Google\Chrome\User Data\Default')
    options.add_argument(r'--user-data-dir=C:\Users\<<Computer Name>>\AppData\Local\Google\Chrome\User Data\Default')
    options.add_argument('--profile-directory=Default')
    s = Service(os.path.join(os.path.realpath(os.getcwd()), 'chrome-driver', 'chromedriver.exe'))
    
    def __init__(self):
        self.data = []
        # To check if the tweet is the last one, the upper bound is 120
        self.none_count = 0
        self.driver = webdriver.Chrome(service=TweetScraper.s, options=TweetScraper.options)
        self.wait = WebDriverWait(self.driver, 45)

    def access(self, url):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def watch(self):
        while True:
            print(get_status(self.driver))
            time.sleep(5)


if __name__ == '__main__':
    
    url = "https://twitter.com/"
    ts = TweetScraper()
    ts.access(url=url)
    ts.watch()
    ts.close()
