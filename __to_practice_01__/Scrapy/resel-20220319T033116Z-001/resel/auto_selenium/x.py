"""
* Info

- Anaconda3
- python 3.8.12

간단하게 쓰이는 crawling 모듈입니다.
scrapy 를 활용하였고, 크게 움직이지 않는 selenium까지 사용이 가능합니다.
(여러가지 parse를 삽입해서 selenium은 scrapy 모듈에서 오류가 많아 selenium 코드를 직접 작성하여 사용하는 것이 좋을 것 같습니다.)
"""

# Module import
import scrapy
import scrapy
import sys
import os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
sys.path.append('../')
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import importlib
import chrome_driver_auto

class XSpider(scrapy.Spider):
    
    """
    사용법은 terminal scrapy crawl {지정명} 입니다. (해당 폴더 경로로 이동해야 됩니다.)
    해당 파일을 예시로 들면
    scrapy crawl FF
    로 실행합니다.
    """
    name = 'FF'
    
    ##  start url
    """
    selenium이 시작할 최초의 url입니다.
    """
    start_urls = ['https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg=1']
    
    
    # fixed (selenium)
    """
    __init__함수 내에서는 Chrome_driver를 각자의 컴퓨터에 설치되어있는 Chrome 버전에 맞게 driver를 설치하고,
    Chrome_driver의 경로를 반환합니다.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        driver_path = chrome_driver_auto.Chrome_driver.install_driver_path()
        
        ############## CHROME OPTION ##############
        """
        Chrome Driver Option입니다.
        Selenium이 작동할때 적용되는 option입니다.
        """
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # chrome_options.add_argument(f"--window_size")        
        

        self.driver = webdriver.Chrome(executable_path = driver_path, chrome_options=chrome_options)
    
   
    """
    Parse 함수부터 selenium을 작동하기 위한 코드가 실행됩니다.
    """ 

    def parse(self,response):
        

        ############### start_selenium ##############
        """ 
        selenium이 최초 url을 받아 실행합니다.
        """
        
        self.driver.get(self.start_urls[0])


        ############### movement setting ############    
        """
        여기서 부터 Selenium에서 작동할 동적 코드를 작성하면 됩니다.
        """
        
        btn = self.driver.find_element_by_xpath('//*[@id="content"]/section[4]/div[2]/nav/button[2]')
        btn.click()
        time.sleep(1) 



        ############### Crawling Object setting #####
        """
        crawling 할 페이지로 움직인 이후,
        가져올 item을 지정하면 됩니다.
        """
        
        product = response.css('li.product-grid__item')
        for item in product:
            yield{
                'name' :item.css('p.product-card__meta::text').get()
                    }
    
    ## SETTING ##
    
        """
        Crawling에 필요한 settings과
        저장방식을 설정하는 곳입니다.
        """
    custom_settings = {
        
        # Detour selenium robots
        ## Invaild page crawling == false
        'ROBOTSTXT_OBEY' : False,
        ## take time to download for detour robots
        'DOWNLOAD_DELAY' : 1,
        
        # save se ttings
        'FEEDS' : {
            # Save file name and extension
            'whiskey.csv' : {
                # format : extension
                'format': 'csv'
            }
        }
    }
    

        
    
    
    
    
    
    
    
    
    
    # def start_requests(self):
    #     urls = ['https://movie.naver.com/movie/running/current.nhn']
    #     for url in urls:
    #         yield scrapy.Request(url=url, callback=self.parse)
    # def parse(self, response):
    #     # pass
    #     movie_sels = response.css('ul.lst_detail_t1 > li')
    #     for movie_sel in movie_sels:
    #         title= movie_sel.css('.tit > a::text').get()
    #         print('tit' , title)