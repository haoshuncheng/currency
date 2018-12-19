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
			print("json数据异常\n")
			continue
		exchangetrades_data = json.dumps(exchange_rs['data'])
		cursor = connect['cur']
		cursor.execute("REPLACE INTO exchangetrades(code,info) values('"+record['id']+"','"+exchangetrades_data+"')")
		conn.commit()


if __name__ == "__main__":
	connect = connect1()
	for isinnovation in [0,1]:
		for page in range(1,11):
			url = "https://dncapi.feixiaohao.com/api/exchange/web-exchange?pagesize=100&type=all&webp=1"+"&isinnovation="+str(isinnovation)+"&page="+str(page)
			get_list(url,isinnovation)