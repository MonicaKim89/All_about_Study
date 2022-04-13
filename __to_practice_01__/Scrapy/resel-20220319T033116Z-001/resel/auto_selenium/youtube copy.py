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

class XSpider(scrapy.Spider):
    name = 'YYYY'
    
    def start_requests(self):
        
        keywords = [parse.quote("금연정책")]
        
        for keyword in keywords:
            yield SeleniumRequest(
            url='https://www.youtube.com/results?search_query={}&sp=CAISAhAB'.format(keyword),
            callback=self.parse_result,
            wait_time =3,
            screenshot=True
            )

    
    def parse_result(self,response):
        youtubeDateSearchKey = re.compile('.+(?=전)')
        driver = response.request.meta['driver']
        body = driver.find_element_by_css_selector('body')
        while True:
            body = driver.find_element_by_css_selector('body')
            if driver.find_element_by_id("message").text.strip() == '결과가 더 이상 없습니다.':               
                break
            body.send_keys(Keys.PAGE_DOWN)
            
        
        
        soup = bs(driver.page_source, 'html.parser')
        title = soup.select('a#video-title') # 유튜브 동영상 제목
        video_url = soup.select('a#video-title') # 유튜브 동영상 URL
        yDate = soup.select('a#video-title') # 유튜브 업로드 날짜
        
        title_list = [] # 유튜브 제목을 저장할 List
        url_list = [] # 유튜브 URL을 저장할 List
        date_list = [] # 유튜브 콘텐츠 업로드 날짜를 저장할 List
        
        for i in range(len(title)):
            yTitle= title[i].text.strip()
            print(yTitle)
            yTitle = re.sub(r"[^ㄱ-ㅎ|ㅏ-ㅣ|가-힣|A-Z|a-z|0-9| ]", " ", yTitle)
            yTitle = re.sub(" {2,}", " ", yTitle)
            if len(yTitle) < 2:
                continue
            urlDate= yDate[i].get('aria-label')
            youtubeDateOrg = youtubeDateSearchKey.search(urlDate)
            
            # for 문을 2번 돌릴 필요가 없을 것 같아서 수정해서 작성해봄
            # url = '{}{}'.format('https://www.youtube.com',video_url[i].get('href'))
            url_list.append('{}{}'.format('https://www.youtube.com',video_url[i].get('href')))
            
            try:
                uDate = youtubeDateOrg.group().split(' ')[-2] + " 전"
                # print(uDate)
                title_list.append(yTitle)
                date_list.append(uDate)
                # title_list.append(yTitle)
                # date_list.append(uDate)
            except: 
                yTitle = 'Null'
                uDate = 'Null'
                title_list.append("Null")
                date_list.append("Null")
                # title_list.append("Null")
                # date_list.append("Null")
        
        for title, url, date in zip(title_list, url_list, date_list):
            yield {
                    '제목': title,
                    '주소': url,
                    '날짜': date
                
            }
        response = response.refresh()
    
    
    # Save_path = 'C:/Dev/NLP/Crawling/Scrapy/scrapy/comment/real/data/'
    Save_path = '../../../../comment/real/data/' # 절대경로 사용 불가 ㅠ
    Save_file_name = 'youtube_urls' 
    Save_extension = 'csv'
    
    if not os.path.exists(Save_path):
        os.makedirs(Save_path)
        
    if not os.path.exists('../Log/'):
        os.makedirs('../Log/')
        
    
    
    
    
    custom_settings = {
        
        # Detour selenium robots
        ## Invaild page crawling == false
        'ROBOTSTXT_OBEY' : False,
        ## take time to download for detour robots
        'DOWNLOAD_DELAY' : 1,
        'SELENIUM_DRIVER_ARGUMENTS' : [
            # '--headless',
            '--window-size=1920,1080'
        ],
        'LOG_LEVEL' : 'INFO',
        'LOG_STDOUT' : True,
        'LOG_FILE' : '../Log/Log.txt',
        # save settings
        
        ## scrapy crawl name -o {filename.extension}
        'FEEDS' : {
            # Save file name and extension
           Save_path + Save_file_name + '.' + Save_extension : {
                # format : extension
                'format': Save_extension
            }
        }
    }            
