# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousefunItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    connect = scrapy.Field()
    size = scrapy.Field()
    content = scrapy.Field()
    detial = scrapy.Field()
