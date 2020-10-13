import scrapy
import sqlite3
import urllib.parse
from eBay.items import EbayItem

class eBaySpider(scrapy.Spider):
	name = 'ebay'

	# start_urls = 'https://www.ebay.com/b/Trek-Bikes/177831/bn_1966928'
	def start_requests(self):

		brand_url = 'https://www.ebay.com/sch/i.html?_oaa=1&_dcat=177831&Brand={}&_sop=15&_blrs=recall_filtering&_fsrp=1&_sacat=0&_nkw=bikes&_from=R40&rt=nc'
		
		conn = sqlite3.connect('/Users/thomasdodge/Desktop/PythonProjects/BikeProject/SQL/ebay_bike_brands.sqlite')
		cur = conn.cursor()
		cur.execute("""SELECT DISTINCT brand
						FROM brands 
						WHERE scraped_time = '2020-03-16' AND brand = 'Cannondale'
							-- brand NOT IN ('Unbranded','Not Specified','Dr. Gustav Klein','Fitbikeco.','State Bicycle Co.')
						ORDER BY 1""")
		lst = cur.fetchall()
	
		for item in lst:
			item = item[0].strip()
			item = urllib.parse.quote(str(item))
			item = urllib.parse.quote(str(item))
			item = item.replace('-','%252D')
			yield scrapy.Request(brand_url.format(item))

	def parse(self, response):

		items = EbayItem()

		all_listings = response.css('li.s-item')

		for listing in all_listings:	
			title = listing.css('h3.s-item__title::text').extract()
			price = listing.css('span.s-item__price').extract()
			link = listing.css('a.s-item__link::attr(href)').re('^h\S+/[0-9]+\?')
			page = response.request.url

			# if title is not None:
			items['title'] = title
			items['price'] = price
			items['link'] = link
			items['page'] = page
	
			yield items

		next_page = response.css('a.pagination__next::attr(href)').extract_first() 

		if next_page is not None:
			yield response.follow(next_page, callback=self.parse)

	


# The below code uses a different starting URL that includes "Brand={}"

# This syntax allows the program to go into a SQLite table that has a list of all bike brands available on eBay and -
# loop through the results of each brand in an attempt to extract all listings for all brands

	# def start_requests(self):
	# 	brand_url = 'https://www.ebay.com/sch/i.html?_oaa=1&_dcat=177831&Brand={}&_sop=15&_blrs=recall_filtering&_fsrp=1&_sacat=0&_nkw=bikes&_from=R40&rt=nc'
		
	# 	conn = sqlite3.connect('/Users/thomasdodge/Desktop/PythonProjects/BikeProject/SQL/ebay_bike_brands.sqlite')
	# 	cur = conn.cursor()
	# 	cur.execute("""SELECT DISTINCT brand
	# 					FROM brands 
	# 					WHERE scraped_time = '2020-03-16' AND brand = 'Trek'
	# 						-- brand NOT IN ('Unbranded','Not Specified','Dr. Gustav Klein','Fitbikeco.','State Bicycle Co.')
	# 					ORDER BY 1""")
	# 	lst = cur.fetchall()
		
	# 	for item in lst:
	# 		item = item[0].strip()
	# 		item = urllib.parse.quote(str(item))
	# 		item = urllib.parse.quote(str(item))
	# 		item = item.replace('-','%252D')
	# 		yield scrapy.Request(brand_url.format(item))
