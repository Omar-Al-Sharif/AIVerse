# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Article(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    published_time = scrapy.Field()
    modified_time = scrapy.Field()
    outlet = scrapy.Field()
