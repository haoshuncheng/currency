import requests
import numpy as np
import time
from rank_data import *
def run():
	connect = connect1()
	cursor = connect['cur']
	connect = connect['con']
	url = 'https://api.binance.com/api/v1/ticker/price'
	data = get_json(url)
	if not data:
		return
	coin_avg = np.mean([float(x['price']) for x in data])
	coin_type = 1
	coint_second = time.time()
	print([coin_type,coin_avg,coint_second])
	sql = "insert into coin_price(type,price,second) values(%s,%s,%s)"
	cursor.execute(sql,[coin_type,coin_avg,coint_second])
	connect.commit()

def get_json(url):
	rs = requests.get(url)
	if rs.status_code == requests.codes.ok:
		return rs.json()



if __name__ == '__main__':
	run()