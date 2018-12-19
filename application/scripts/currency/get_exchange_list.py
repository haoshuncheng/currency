#获取交易所列表
import requests
from lxml import etree
import sys
import time
import json
import re
from rank_data import *

def get_list(url,isinnovation):
	print(url)

	rs = get_requests(url, 'json')
	if rs == False:
		print("list列表失败\n")
		return False
	if 'code' not in rs or rs['code']!='200' or 'data' not in rs or len(rs['data'])==0:
		print(url)
		print("json数据异常\n")
		return False
	for record in rs['data']:
		record['isinnovation'] = isinnovation
		record['labels_id'] = 0 if not record['labels_id'] else record['labels_id']
		record['isfocus'] = 0 if not record['isfocus'] else 1
		record['isshare'] = 0 if not record['isshare'] else 1
		write(connect['con'],'exchange',record)
		exchangeTrades_url = "https://dncapi.feixiaohao.com/api/exchange/exchangetrades?code="+record['id']+"&webp=1"
		exchange_rs = get_requests(exchangeTrades_url, 'json')
		if exchange_rs == False:
			print("list列表失败\n")
			continue
		if 'code' not in exchange_rs or exchange_rs['code']!='200' or 'data' not in exchange_rs or len(exchange_rs['data'])==0:
			print(exchangeTrades_url)
			print("json数据异常\n")
			continue
		exchangetrades_data = json.dumps(exchange_rs['data'])
		cursor = connect['cur']
		cursor.execute("REPLACE INTO exchangetrades(code,info) values('"+record['id']+"','"+exchangetrades_data+"')")
		connect['con'].commit()

		coin_pairs_url = "https://dncapi.feixiaohao.com/api/exchange/coinpair_list"
		data = {"code":record['id'],"page":1,"pagesize":1000,"webp":1}
		coin_pairs_rs = post_requests(coin_pairs_url,json.dumps(data))
		if coin_pairs_rs == False:
			print("list列表失败\n")
			continue
		if 'code' not in coin_pairs_rs or coin_pairs_rs['code']!='200' or 'data' not in coin_pairs_rs or len(coin_pairs_rs['data'])==0:
			print(data)
			print("json数据异常\n")
			continue
		coin_pairs_data = coin_pairs_rs['data']
		for coin_record in coin_pairs_data:
			coin_record['code'] = record['id']
			write(connect['con'],'coin_pairs',coin_record)




if __name__ == "__main__":
	connect = connect1()
	for isinnovation in [0,1]:
		for page in range(1,11):
			url = "https://dncapi.feixiaohao.com/api/exchange/web-exchange?pagesize=100&type=all&webp=1"+"&isinnovation="+str(isinnovation)+"&page="+str(page)
			get_list(url,isinnovation)