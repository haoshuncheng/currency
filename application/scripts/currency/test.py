import requests
import numpy as np

def run():
	global baseurl
	rs = requests.get(baseurl)
	data = rs.json()
	record = [float(x['price']) for x in rs]
	avg = np.mean(record)
	print(avg)



if __name__ == '__main__':
	baseurl = 'https://api.binance.com/api/v1/ticker/price'
	run()