import requests 
import re
from time import sleep
from random import uniform
import sqlite3 
from bs4 import BeautifulSoup

# Creates BS object from URL using requests library
def getPage(url):
    session = requests.Session()
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    try:
        req = session.get(url, headers=headers)
    except requests.exceptions.RequestException:
        return None
    bs = BeautifulSoup(req.text, 'html.parser')
    return bs


# Initial eBay scrape of search results page. Stores data in SQLite DB
def ebayInitial(bs):
	for item in bs.findAll('li', {'class': 's-item'}):
		try:
			item_link = item.find('a').get('href')
			item_link_short = re.findall('^h\S+/[0-9]+\?',item_link)[0]
		except:
			continue
	
		cur.execute('''INSERT OR IGNORE INTO Item_List (source, item_link_short)
                VALUES (?, ?)''', ('eBay', item_link_short))
		conn.commit()


# Create SQLite DB
conn = sqlite3.connect('ebay_scrape.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS Item_List')
cur.execute('''CREATE TABLE item_list (source TEXT, item_link_short TEXT, UNIQUE(item_link_short))''')

# URL & page number variable to iterate through results pages
page_counter = 1
url = 'https://www.ebay.com/sch/bikes&_pgn={}'.format(page_counter)

# Iterates through results pages and runs scrape function on each
for i in range(100):
	print('Scraping Page: ', page_counter)
	sleep(uniform(2,5))
	ebayInitial(getPage(url))
	page_counter = page_counter + 1
	

#SCRAP CODE
#price = item.find('span', {'class': 's-item__price'}).get_text()
#title = item.find('h3').get_text()
#ebay_id = re.findall('^h\S+/([0-9]+)\?',item_link)[0]

# AVOIDING GETTING BLOCKED BY SITE
# Need to change/rotate both User Agents & IP Addresses. Multiple requests from different user agents with the same IP Address will be suspicous
# Change/rotate headers/user agents when making HTTP requests to site server. See pg 219 in Web Scraping book for more details
# https://developers.whatismybrowser.com/useragents/explore/
# Rotate proxies & IP adresses to avoid being blocked
# Potential sources of proxies & IPs: crawlera, scraperapi, & https://homeip.io/ - https://www.scraperapi.com/blog/best-10-free-proxies-and-free-proxy-lists-for-web-scraping/
# Be aware of how cookies are used to track users on sites and block IPs
# https://www.scrapehero.com/how-to-rotate-proxies-and-ip-addresses-using-python-3/


# STORING ATTRIBUTES 
# For item description on item link page - can create a field that is a dictionary/JSON -
# Provides felxibility if some items don't have certain attributes. Capture all attributes
# available for that item on initial pass and decide how to handle later, while not 
# impacting data schema (pg 50 in "Web Scraping with Python" book)

