#module import
import scrapy
import pandas as pd
import importlib
import os
import sys
import time

# system path append
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
# 
# from scrapy_selenium import SeleniumRequest

# Spider Class
class TestModuleSpider(scrapy.Spider):
    name = 'test'

    def start_requests(self):
        
        # get_mod 
        global get_variables
        def get_variables(input_module):
            mod =  importlib.import_module(input_module)
            return mod
        
        global input_module, pass_py
        input_module = self.input_module
        pass_py = get_variables(input_module)
        
        ## one _ url
        urls = pass_py.crawl_form.url()
        for url in urls:
            yield scrapy.Request(url,callback=self.parse)   
            
            
    def parse(self, response):
        # pass_py = get_variables(input_module)
        pass_py.crawl_form.parse(response)
        # selenium_url = pass_py.crawl_form.url()
        # self.driver.get(selenium_url)
        # time.sleep(3)
        
                
    

      
