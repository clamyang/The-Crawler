# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    house_title = scrapy.Field()
    final_url = scrapy.Field()
    house_located = scrapy.Field()
    house_code = scrapy.Field()
    house_price = scrapy.Field()
    contact_name = scrapy.Field()
    phone_num = scrapy.Field()
    lease_way = scrapy.Field()
    room_info = scrapy.Field()
    house_size = scrapy.Field()
    house_direction = scrapy.Field()
