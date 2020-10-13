# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import datetime


class Ebayscrapy2Pipeline(object):

	def __init__(self):
		self.create_connection()
		self.create_table()

	def create_connection(self):
		self.conn = sqlite3.connect('/Users/thomasdodge/Desktop/PythonProjects/BikeProject/SQL/ebay2.sqlite')
		self.cur = self.conn.cursor()

	def create_table(self):
		self.cur.execute("""DROP TABLE IF EXISTS daily_listings_20201005""")
		self.cur.execute("""CREATE TABLE daily_listings_20201005(scraped_time text, page text, title text, price text, link text)""")

	def process_item(self, item, spider):
		self.store_db(item)

	def store_db(self,item):
		self.cur.execute("""INSERT INTO daily_listings_20201005 values (?,?,?,?,?)""", (datetime.datetime.now(), item['page'], item['title'][0], item['price'][0], item['link'][0]))
		self.conn.commit()

