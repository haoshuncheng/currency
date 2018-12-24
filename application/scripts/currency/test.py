import requests
import numpy as np

def run():
	global baseurl
	rs = requests.get(baseurl)
	rs = rs.json()
	rs = [float(x['price']) for x in rs]
	print(rs)
	x = np.mean(rs)
	print(x)



if __name__ == '__main__':
	baseurl = 'https://api.binance.com/api/v1/ticker/price'
	run()