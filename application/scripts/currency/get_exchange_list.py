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
		print(record)
		time.sleep(3)
		# code = record['']
		# sql = "replace into exchange values()"





if __name__ == "__main__":
	connect = connect1()
	for isinnovation in [0,1]:
		for page in [1,10]:
			url = "https://dncapi.feixiaohao.com/api/exchange/web-exchange?pagesize=100&type=all&webp=1"+"&isinnovation="+str(isinnovation)+"&page="+str(page)
	get_list(url,isinnovation)