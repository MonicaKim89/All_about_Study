import scrapy
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import scrapy
import logging
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.webdriver.common.keys import Keys
import re
from urllib import parse
from selenium import webdriver
import os
import pandas as pd
import time
from selenium.common.exceptions import NoSuchElementException


class SelSpider(scrapy.Spider):
    name = 'sel'
    # allowed_domains = ['x']
    # start_urls = ['http://x/']

    
    def start_requests(self):
        ### Drive 적용
        options = Options()
        options.add_argument('--headless') #headless모드 브라우저가 뜨지 않고 실행됩니다.
        # options.add_argument('--window-size= x, y') #실행되는 브라우저 크기를 지정할 수 있습니다.
        # options.add_argument('--start-maximized') #브라우저가 최대화된 상태로 실행됩니다.
        # options.add_argument('--start-fullscreen') #브라우저가 풀스크린 모드(F11)로 실행됩니다.
        # options.add_argument('--blink-settings=imagesEnabled=false') #브라우저에서 이미지 로딩을 하지 않습니다.
        # options.add_argument('--mute-audio') #브라우저에 음소거 옵션을 적용합니다.
        # options.add_argument('incognito') #시크릿 모드의 브라우저가 실행됩니다.
        options.add_experimental_option("excludeSwitches", ["enable-logging"]) #selenium 작동 안될 때
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(),chrome_options=options)    
        
        
        ## 여러 url 적용
        # url_file = pd.read_csv(r'C:\Dev\NLP\Crawling\Scrapy\scrapy\comment\real\data\youtube_urls.csv')
        # url_list = list(url_file['주소'])
        # for url in url_list:
        #     self.driver.get(url)
        url = 'https://www.youtube.com/watch?v=6z5E6sn7Jv8'
        self.driver.get(url)    
        ## selenium movement 설정
        count = 1

        # info = self.driver.fine_element_by_css_selector('.style-scope ytd-video-primary-info-renderer')
        
        # for i in range(len(url_list)):
        if count:
            try:
                self.driver.implicitly_wait(0.5)
                self.driver.find_element_by_css_selector('#main > div > ytd_button-renderer').click()
                count -= 1
            except:
                pass
       
        last_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
            time.sleep(1)
            new_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")
            if new_page_height == last_page_height:
                break
            last_page_height = new_page_height
            time.sleep(1)
            
        yield scrapy.Request(url=url, callback=self.parse)        
        ## movement stop
        
    def parse(self, response):
        # body = self.driver.find_element_by_tag_name('body')
        ### output
        soup0 = self.driver.page_source
        soup = bs(soup0,'lxml')
        
        users = soup.select("div#header-author > h3 > #author-text > span")
        comments = soup.select('yt-formatted-string#content-text') #댓글만
        comment_list = []
        for i in range(len(users)):
            str_temp = str(comments[i].text)
            comment_list.append(str_temp)
        
        for i in comment_list:
            # print(i)
            yield{
                'comment' : i
            }
    custom_settings = {
        
        # Detour selenium robots
        ## Invaild page crawling == false
        'ROBOTSTXT_OBEY' : False,
        ## take time to download for detour robots
        'DOWNLOAD_DELAY' : 1,
        
        # save se ttings
        'FEEDS' : {
            # Save file name and extension
            'youtube_crawl.csv' : {
                # format : extension
                'format': 'csv'
            }
        }
        }               
                
                
        