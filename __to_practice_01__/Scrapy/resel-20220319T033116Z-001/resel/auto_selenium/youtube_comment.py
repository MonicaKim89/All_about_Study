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
import time
from selenium.common.exceptions import NoSuchElementException

class YoutubeCommentSpider(scrapy.Spider):
    
    name = 'youtube_comment'
    
    # allowed_domains = ['x']
    # start_urls = ['http://x/']
    def start_requests(self):
        
        url_file = pd.read_csv(r'C:\Dev\NLP\Crawling\Scrapy\scrapy\comment\real\data\youtube_urls.csv')
        url_list = list(url_file['주소'])
        urls = [i.split('https://www.youtube.com/')[1] for i in url_list]
        for url in urls:
            yield SeleniumRequest(
            url = 'https://www.youtube.com/'+url,
            callback = self.parse_result,
            wait_time = 3
            )
        
    def parse_result(self, response):
        driver = response.request.meta['driver']
        
        ##### movement start
        
        ### page check
        body = driver.find_element_by_tag_name('body')
        last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        
        ### page-down
        while True:
            driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
            time.sleep(2)
            new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_page_height == last_page_height:
                break
            last_page_height = new_page_height
 
        ###### movement stop
        
        ##### Output
        soup0 = driver.page_source
        soup = bs(soup0,'html.parser')
        
        ### Exception
        commentNumXpath = """//*[@id="count"]/yt-formatted-string"""
        try:
            commentNum = driver.find_element_by_xpath(commentNumXpath).text
       
        except NoSuchElementException as e:
            for i in range(5):
                body.send_keys(Keys.PAGE_UP)
            time.sleep(1)
            try:
                commentNum = driver.find_element_by_xpath(commentNumXpath).text
            except NoSuchElementException as e:
                print('e')
            
    
        comment_list = []
        commentXpath = """/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[{0}]/ytd-comment-renderer/div[1]/div[2]/ytd-expander/div/yt-formatted-string"""
        comment = driver.find_element_by_xpath(commentXpath).text
        comment = re.sub(r"[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|A-Z|a-z|0-9| ]", " ", comment)
        comment = re.sub(" {2,}", " ", comment)
        comment_list.append(comment)
        
        for comment in comment_list:
            yield{
                '댓글' : comment
            }
        
        ##### response refresh
        
        
    # # Save_path = 'C:/Dev/NLP/Crawling/Scrapy/scrapy/comment/real/data/'
    # Save_path = './' # 절대경로 사용 불가 ㅠ
    # Save_file_name = 'youtube_comments' 
    # Save_extension = 'csv'
    
    # if not os.path.exists(Save_path):
    #     os.makedirs(Save_path)
        
    # if not os.path.exists('../Log/'):
    #     os.makedirs('../Log/')
        
    
    
    
    
    custom_settings = {
        
        # Detour selenium robots
        ## Invaild page crawling == false
        'ROBOTSTXT_OBEY' : False,
        ## take time to download for detour robots
        'DOWNLOAD_DELAY' : 1,
        'SELENIUM_DRIVER_ARGUMENTS' : [
            
            # '--headless',
            # '--window-size=1050,1050'
            'excludeSwitches',
            'enable-logging'
        ],
        # 'LOG_LEVEL' : 'INFO',
        # 'LOG_STDOUT' : True,
        # 'LOG_FILE' : '../Log/Log.txt',
        # save settings
        
        ## scrapy crawl name -o {filename.extension}
        # 'FEEDS' : {
        #     # Save file name and extension
        #    Save_path + Save_file_name + '.' + Save_extension : {
        #         # format : extension
        #         'format': Save_extension
        #     }
        # }
    }                    
        