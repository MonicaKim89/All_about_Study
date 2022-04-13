import scrapy
import logging
from scrapy.http import HtmlResponse
from scrapy_selenium import SeleniumRequest

# class SeleniumRequest(scrapy.Request):
#     def __init__(self, wait_time=None, wait_until=None, wait_sleep=None,
#                 screenshot=False, script=None, *args, **kwargs):
        
#         self.wait_time = wait_time
#         self.wait_until = wait_until
#         self.wait_sleep = wait_sleep
#         self.screenshot = screenshot
#         self.script = script
        
#         super().__init__(*args, **kwargs)
        
#     def release_driver(self):
#         middleware = self.meta['middleware']
#         driver = self.meta['driver']
#         if driver:
#             driver.get('about:blank')  # get a blank tab -- ensures next request using driver won't have "stale" content
#             middleware.driver_queue.put(driver)
#             logger.debug(f'Returned driver to the queue ({middleware.driver_queue.qsize()} drivers available)')
#             del self.meta['driver']


class Xspider(scrapy.Spider):
    name = 'XXX'
    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.thewhiskyexchange.com/c/40/single-malt-scotch-whisky?pg=1',
            callback=self.parse_result,
            wait_time =3
        )
    
    def parse_result(self,response):
        driver = response.request.meta['driver']
        driver.find_element_by_xpath('//*[@id="content"]/section[4]/div[2]/nav/button[2]').click()
        response = response.refresh()
        proofs = response.css('li.product-grid__item')
        for proof in proofs:
            yield{
                'name' : proof.css('p.product-card__meta::text').get()
            }
        response.release_driver()
    
        
        
        
        
        
        
        
 

        
