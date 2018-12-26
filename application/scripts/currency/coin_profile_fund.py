#资金流向
import requests
from lxml import etree
import pymysql.cursors
import sys
import time
import json
import re
from get_rank_list import *


def main():
	codes = get_all_codes()
	for code in codes:
		code = code['code']
		querystring['coin_type'] = code
		response = requests.request("GET", url, headers=headers, params=querystring)
		try:
			response = response.json()
			data = response['flow_distribute']
			sql = "replace into coin_fund (code,fund) value('"+code+"','"+json.dumps(data)+"')"
			cursor.execute(sql)
			connect.commit()
			print(code+" ok\n")
		except:
			print(sys.exc_info())
			continue

def get_all_codes():
	cursor.execute("select code from rank")
	return cursor.fetchall()

if __name__ == "__main__":
	db = connect1()
	connect,cursor = [db[x] for x in db]

	headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    'referer': "https://www.aicoin.net.cn/",
    'authority': "www.aicoin.net.cn",
    'scheme': "https",
    'accept': "*/*",
    'cache-control': "no-cache",
    }
	url = "https://www.aicoin.net.cn/api/coin-profile/fund"
	querystring = {"coin_type":"adcoin","currency":"cny"}
	main()