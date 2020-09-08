import scrapy
import re
from ..items import HousefunItem

class HouseinfoSpider(scrapy.Spider):
    name = 'houseinfo'
    # allowed_domains = ['rent.housefun.com']
    # start_urls = ['https://rent.housefun.com.tw/']
    allowed_domains = ['rent.housefun.com']
    start_urls = ['https://rent.housefun.com.tw/']
    baseUrl = "https://rent.housefun.com.tw/"
    def parse(self, res):
        print("="*30)
        print("in HouseinfoSpider")
        print("res.meta: {}".format(res.keep['continue']))
        if not res.keep['continue'] :
            return
        article_list = res.xpath("//div[@id = 'SearchContent']/article")
        print("=================article_list", article_list)
        for article in article_list:
            title = article.xpath("./div[@class = 'Data']/h3/a/@title").get().strip()
            address = article.xpath("./div[@class = 'Data']/address/text()").get().strip()
            price = article.xpath(".//li[@class='InfoList'][1]//span[2]/text()").get().strip()
            connect = article.xpath(".//li[@class='InfoList'][3]//span[1]/text()").get().strip()
            size = article.xpath(".//li[@class='InfoList'][2]//span[2]/text()").get().strip()
            content = article.xpath(".//span[@class='sectionList']//text()").getall()
            content = re.sub(r'\s+',"","".join(content))
            detial = article.xpath(".//li[@class='detailist']//a[2]/@href").get().strip()
            detial = res.urljoin(detial)
            print("="*30)
            print("address: " , address)
            print("title: " , title)
            print("price: " , price)
            print("connect: " , connect)
            print("size: " , size)
            print("content: " , content)
            print("detial: " , detial)
            print("="*30)
            house = HousefunItem(
                title = title, address = address, price = price, size = size, connect = connect, content = content,
                detial = detial
            )
            yield house
        yield scrapy.Request(self.baseUrl, callback=self.parse, dont_filter=True)
            


            
