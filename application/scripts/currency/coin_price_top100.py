import requests
import numpy as np
import time
from rank_data import *
########获取 币 安  top100 币 价格 /每秒
def run():
	data = get_json(url)
	
	if not data:
		return
	coin_type = 1
	coint_second = str(int(time.time()))
	coin_avg = str(np.mean([float(x['price']) for x in data]))
	print([coin_type,coin_avg,coint_second])
	sql = "replace into coin_price(type,price,second) values("+str(coin_type)+",'"+coin_avg+"','"+coint_second+"')"
	cursor.execute(sql)
	connect.commit()


def get_json(url):
	rs = requests.get(url)
	if rs.status_code == requests.codes.ok:
		return rs.json()


if __name__ == '__main__':
	connect = connect1()
	cursor = connect['cur']
	connect = connect['con']
	url = 'https://api.binance.com/api/v1/ticker/price'
	while True:
		run()
		