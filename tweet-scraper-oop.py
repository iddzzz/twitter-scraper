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


class TweetScraper:
    options = webdriver.ChromeOptions()
    # For remembering the previous login session
    # options.add_argument(r'--user-data-dir=C:\Users\Saidzzz\AppData\Local\Google\Chrome\User Data\Default')
    options.add_argument(r'--user-data-dir=C:\Users\<<Computer Name>>\AppData\Local\Google\Chrome\User Data\Default')
    options.add_argument('--profile-directory=Default')
    options.headless = True  # To make browser disappear
    s = Service(os.path.join(os.path.realpath(os.getcwd()), 'chrome-driver', 'chromedriver.exe'))
    

    def __init__(self):
        self.data = []
        # To check if the tweet is the last one, the upper bound is 120
        self.none_count = 0
        self.driver = webdriver.Chrome(service=TweetScraper.s, options=TweetScraper.options)
        self.wait = WebDriverWait(self.driver, 45)

    def access(self, url):
        self.driver.get(url)

    def check(self, delay=5):
        try:
            self.wait.until(ec.presence_of_element_located(
                (By.XPATH, xpath['tweet'])))
            print("We've entered")
        except NoSuchElementException:
            print("No element ternyata")
            self.driver.close()
        time.sleep(delay)

    # Take tweets from page
    def take_tweets(self):
        return self.driver.find_elements(By.XPATH, xpath['tweet'])

    # retrieve data from a tweet
    def retrieve_data(self, tweet):
        # there was a time when no name there
        try:
            name = tweet.find_element(By.XPATH, xpath['name']).text
        except NoSuchElementException:
            name = ''

        # there was a time when no username there
        try:
            username = tweet.find_element(By.XPATH, xpath['username']).text
        except NoSuchElementException:
            username = ''

        # there are advertisment tweets without date
        try:
            date = tweet.find_element(By.XPATH, xpath['date']).text
        except NoSuchElementException:
            date = NaN

        # there are tweets with reply_to elements, but not all
        try:
            reply_to = tweet.find_element(By.XPATH, xpath['reply_to']).text
        except NoSuchElementException:
            reply_to = NaN

        content = tweet.find_element(By.XPATH, xpath['content']).text
        reply = tweet.find_element(By.XPATH, xpath['reply']).text
        retweet = tweet.find_element(By.XPATH, xpath['retweet']).text
        like = tweet.find_element(By.XPATH, xpath['like']).text
        id = ''.join(
            [name.replace(' ', ''), str(date).replace(' ', '').replace(',', ''), content[:7] if bool(content) else ''])
        # print(f'{name} | {username} | {date}')
        # print(f'Replying to: {reply_to}')
        # print(f'{content}')
        # print(f'Number of reply: {int(reply) if bool(reply) == True else 0}')
        # print(f'Number of retweet: {int(retweet) if bool(retweet) == True else 0}')
        # print(f'Number of like: {int(like) if bool(like) == True else 0}')
        koleksi = {'id': id, 'name': name, 'username': username,
                   'date': date, 'reply_to': reply_to, 'content': content,
                   'reply': reply, 'retweet': retweet, 'like': like}

        if len(self.data) == 0:
            self.data.append(koleksi)
            print('-', id)
        elif len(self.data) < 20:
            if koleksi in self.data:
                self.none_count += 1
            else:
                self.data.append(koleksi)
                self.none_count = 0
                print('-', id)
        else:
            if koleksi in self.data[-20:]:
                self.none_count += 1
            else:
                self.data.append(koleksi)
                self.none_count = 0
                print('-', id)

    def down(self):
        ActionChains(self.driver).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()

    def close(self):
        self.driver.close()

    def tweet_loop(self, tweets):
        for tweet in tweets:
            self.retrieve_data(tweet=tweet)

    def to_csv(self, name: str):
        df = pd.DataFrame(self.data)
        df.to_csv(f"{os.path.join(os.path.realpath(os.getcwd()), 'data', name)}", index=False)

    def scrape(self, delay=2):
        i = 1
        while True:
            try:
                self.tweet_loop(self.take_tweets())
                self.down()
            except Exception as why:
                print('Something wrong!')
                print(why)
                break
            print(f'Iteration: {i} | Data Count: {len(self.data)} | None Count: {self.none_count}')
            if self.none_count > 120:
                print('All data has been scraped completely')
                break
            i += 1
            time.sleep(delay)


if __name__ == '__main__':
    word = input('Keyword: ')
    tanggal = input('Since (date): ')
    bulan = input('Since (month) (in number e.g. 01, 02, ... ): ')
    year = input('Since (year): ')
    next_tanggal = input('Until (date): ')
    next_bulan = input('Until (month) (in number e.g. 01, 02, ... ): ')
    next_year = input('Until (year): ')
    output_name = input('Save as (with .csv): ')
    url = f"https://twitter.com/search?q=({word})%20until%3A{next_year}-{next_bulan}-{next_tanggal}%20since%3A{year}-{bulan}-{tanggal}&src=typed_query&f=live"
    ts = TweetScraper()
    ts.access(url=url)
    ts.check()
    ts.scrape()
    ts.to_csv(output_name)
    ts.close()
