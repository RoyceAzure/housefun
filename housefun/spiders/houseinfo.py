import scrapy
import re


class HouseinfoSpider(scrapy.Spider):
    name = 'houseinfo'
    # allowed_domains = ['rent.housefun.com']
    # start_urls = ['https://rent.housefun.com.tw/']
    allowed_domains = ['rent.housefun.com']
    start_urls = ['https://rent.housefun.com.tw/']

    def parse(self, response):
        article_list = response.xpath("//div[@id = 'SearchContent']/article")
        for article in article_list:
            title = article.xpath("./div[@class = 'Data']//a/@title/text()").get()
            print("="*30)
            print("title: " , title)
            print("="*30)
            break
