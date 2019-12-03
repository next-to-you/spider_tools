# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdBookItem(scrapy.Item):
    # define the fields for your item here like:
    class_3_name = scrapy.Field()
    class_1_name = scrapy.Field()
    class_2_name = scrapy.Field()
    class_4_name = scrapy.Field()

    name = scrapy.Field()
    big_name = scrapy.Field()
    small_name = scrapy.Field()
    img_link = scrapy.Field()
    price = scrapy.Field()
    publisher = scrapy.Field()
    author = scrapy.Field()
    publish_time = scrapy.Field()



