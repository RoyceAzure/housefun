import scrapy
import re


class HouseinfoSpider(scrapy.Spider):
    name = 'houseinfo'
    # allowed_domains = ['rent.housefun.com']
    # start_urls = ['https://rent.housefun.com.tw/']
    allowed_domains = ['rent.housefun.com']
    start_urls = ['https://rent.housefun.com.tw/']

    def parse(self, res):
        print("="*30)
        print("in HouseinfoSpider")
        for response in res:
            article_list = response.xpath("//div[@id = 'SearchContent']/article")
            print("=================article_list", article_list)
            for article in article_list:
                print("=================article_list", article_list)
                title = article.xpath("./div[@class = 'Data']/h3/a/@title").get()
                print("="*30)
                print("title: " , title)
                print("="*30)
            
