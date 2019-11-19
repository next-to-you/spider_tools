# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    city = scrapy.Field()
    month = scrapy.Field()
    day = scrapy.Field()
    aqi = scrapy.Field()
    level = scrapy.Field()
    pm2_5 = scrapy.Field()
    pm10 = scrapy.Field()
    so_2 = scrapy.Field()
    co = scrapy.Field()
    no_2 = scrapy.Field()
    o3_8h = scrapy.Field()

    data_time = scrapy.Field()
    data_source = scrapy.Field()

