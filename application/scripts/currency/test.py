import requests

def run():
	global baseurl
	rs = requests.get(baseurl)
	rs = rs.json()
	x = [x['price'] for x in rs]
	print(x)



if __name__ == '__main__':
	baseurl = 'https://api.binance.com/api/v1/ticker/price'
	run()