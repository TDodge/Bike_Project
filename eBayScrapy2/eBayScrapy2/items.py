# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class Ebayscrapy2Item(scrapy.Item):
	title = scrapy.Field()
	price = scrapy.Field()
	link = scrapy.Field()
	page = scrapy.Field()