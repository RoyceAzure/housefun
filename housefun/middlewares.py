# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import time
from scrapy.http.response.html import HtmlResponse
from selenium.webdriver.common.by import By

class HousefunSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HousefunDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self):
        self.driverPath = "F:/Workspace/JackRabbit/Myproject/HouseFun/housefun/chromedriver.exe"
    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumHousefunSpiderMiddleware(object):
    index = 1
    
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r"F:\Workspace\JackRabbit\Myproject\HouseFun\housefun\chromedriver.exe")
        self._limit_page = None
    def process_request(self, request, spider):# 若此處返回response , 則不會走到downloader , 會直接返回
        print("="*30 )
        print("in SeleniumHousefunSpiderMiddleware")
        print("in index : {}".format(SeleniumHousefunSpiderMiddleware.index))
        print("in self._limit_page : {}".format(self._limit_page))
        keep_going = False

        self.driver.get(request.url)

        # response_list = []
          #睡一秒  讓Ajax去抓資料
        time.sleep(1.5)
        if SeleniumHousefunSpiderMiddleware.index <= self.limit_page :
            keep_going = True
        self.driver.execute_script("PM({})".format(SeleniumHousefunSpiderMiddleware.index))
        time.sleep(2.5)
        # button = self.driver.find_element_by_link_text("›")
        # print("button : ", button)
        

        SeleniumHousefunSpiderMiddleware.index = SeleniumHousefunSpiderMiddleware.index+1
        return self.get_source_page(request,keep_going)

        # return self.get_source_page(request)
    def get_source_page(self,request,keep_going):
        source = self.driver.page_source
        response = HtmlResponse(url = request.url, body=source, request=request , encoding='utf-8', meta = {'continue' : keep_going})    
        return response

    def process_exception(self, request, exception, spider):
        print("="*30)
        print(exception)
        print(request)
        print("call process_exception")
    @property
    def limit_page(self):
        if not self._limit_page:
            print("no self._limit_page")
            self._limit_page = self.driver.find_element(By.XPATH, '//span[@id = "PageCount"]').text.split('/')[1]
            self._limit_page = int(self._limit_page)
            print("after self._limit_page : {}".format(self._limit_page))
            return self._limit_page