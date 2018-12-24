import requests
import numpy as np

def run():
	global baseurl
	rs = requests.get(baseurl)
	rs = rs.json()
	x = np.mean([x['price'] for x in rs])




if __name__ == '__main__':
	baseurl = 'https://api.binance.com/api/v1/ticker/price'
	run()