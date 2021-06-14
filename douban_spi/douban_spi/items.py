# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanSpiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title_detail = scrapy.Field()
    author_detail = scrapy.Field()
    author_time_detail =scrapy.Field()
    abstract_detail = scrapy.Field()
    #score_detail = scrapy.Field()
    picture_detail = scrapy.Field()

    reader = scrapy.Field()
    reader_time = scrapy.Field()
    comment = scrapy.Field()
    pass
