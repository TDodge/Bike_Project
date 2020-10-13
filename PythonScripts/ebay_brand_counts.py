import requests
import json
import sqlite3
from datetime import datetime
import re

#  jquery_call:
#  - jquery_call value found in the developer -> network view when clicking "See All" button 
#    under brand list on https://www.ebay.com/sch/i.html?_nkw=bikes.
#  - The "See All" button generates jQuery and the URL below returns all brands and count of listings in each

jquery_call = 'https://www.ebay.com/sch/ajax/refine?no_encode_refine_params=1&_fsrp=1&_aspectname=aspect-Brand&_nkw=bikes&rt=nc&modules=SEARCH_REFINEMENTS_MODEL_V2%3Afa&pageci=8d91c460-5e26-11ea-8f69-74dbd180e998'

r = requests.get(jquery_call)
response = r.json()


# See bottom of file for reference on extracting JSON items
def extract_brand():
	brand_list = []
	
	if response['group'][0]['entries'][3]['entries'][0]['paramKey'] != "Brand":
		return "JSON location change. Revisit JSON response"
	
	else:
		for item in response['group'][0]['entries'][3]['entries']:
			brand = item['label']['textSpans'][0]['text']
			count = int(item['secondaryLabel']['textSpans'][0]['text'][2:][:-1].replace(',',''))
			brand_dict = {'brand': brand, 'count': count}
			brand_list.append(brand_dict)

		return brand_list

def store_data(brand_list):
	conn = sqlite3.connect('/Users/thomasdodge/Desktop/PythonProjects/BikeProject/SQL/ebay_bike_brands.sqlite')
	cur = conn.cursor()
	# cur.execute("""DROP TABLE IF EXISTS brands""")
	# cur.execute("""CREATE TABLE brands(scraped_time text, brand text, count int)""")
	
	for item in brand_list:
		cur.execute("""INSERT INTO brands values (?,?,?)""", (datetime.today().strftime("%Y-%m-%d %H:%M:%S"),item['brand'], item['count']))
	
	conn.commit()
	conn.close()

#Run store_data function if extract_brand() returns a list, else print error message 	
if isinstance(extract_brand(), list):
	store_data(extract_brand())
else:
	print("Error when retrieving JSON data")

	
# # Use the following code to make returned JSON from eBay more readable: 
# print(json.dumps(response['group'][0]['entries'][3]['entries'],indent=2))

# Walk through the JSON to extract the correct fields:
# - Type reveals whether list or dict
# - Len reveals count of items. Number of brands should be ~250
# - print(type(response['group'][0]['entries'][3]['entries']))
# - print(len(response['group'][0]['entries'][3]['entries']))