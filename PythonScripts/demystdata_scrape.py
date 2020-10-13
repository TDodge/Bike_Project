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


url = 'https://demyst.com/products'

bs = getPage(url)

print(bs)

# def company_name(bs):
# 	for item in bs.findAll({}):
# 		print(item)

# company_name(bs)