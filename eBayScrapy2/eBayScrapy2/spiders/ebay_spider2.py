import scrapy
from eBayScrapy2.items import Ebayscrapy2Item
from time import sleep
from random import uniform


class eBaySpider2(scrapy.Spider):
	name = 'ebay2'

	start_urls = ['https://www.ebay.com/b/Trek-Bikes/177831/bn_1966928']

	def parse(self, response):

		items = Ebayscrapy2Item()

		all_listings = response.css('li.s-item')

		for listing in all_listings:	

			items['title'] = listing.css('h3.s-item__title::text').extract()
			items['price'] = listing.css('span.s-item__price::text').extract()
			items['link'] = listing.css('a.s-item__link::attr(href)').re('^h\S+/[0-9]+\?')
			items['page'] = response.request.url

			yield items

##
		next_page = response.css('a.ebayui-pagination__control[rel="next"]::attr(href)').extract_first()
		print(next_page)

		if next_page is not None:
			sleep(uniform(3,6))
			yield response.follow(next_page, callback=self.parse)












