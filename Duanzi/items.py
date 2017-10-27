# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DuanziItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = scrapy.Field()
    digg_count = scrapy.Field()
    bury_count = scrapy.Field()
    repin_count = scrapy.Field()
    comment_count = scrapy.Field()
    pic_url_list = scrapy.Field()

    #用于存储所有图片的路径,用逗号隔开
    path = scrapy.Field()

    #用于区分到底是段子还是图片
    type = scrapy.Field()

