import requests
import pymysql.cursors
import sys
import time
import json


	

def handurl(url,curPage):
	global headers
	global connect
	full_url = url+"&page="+str(curPage)
	rs = requests.get(full_url, headers=headers)
	if rs.status_code != 200:
		print(full_url+" 数据请求失败\n")
		return
	data = rs.json()
	records = data['data']
	for record in records:
		print(record)
		time.sleep(5)
	maxPageSize = data['maxpage']
	curPage = data['currpage']
	if int(curPage) <= int(maxPageSize):
		handurl(url,curPage)


def connect1():
	connect = pymysql.Connect(
		host='localhost',
	    port=3306,
	    user='dev',
	    passwd='1fi923^a3bui*9',
	    db='my_data',
	    charset='utf8'
	)
	cursor = connect.cursor(pymysql.cursors.DictCursor)
	cursor.execute('SET NAMES utf8;')
	cursor.execute('SET CHARACTER SET utf8;')
	cursor.execute('SET character_set_connection=utf8;')
	return {'con':connect, 'cur':cursor}




if __name__ == '__main__':
	connect = connect1()
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	base_url = "https://dncapi.feixiaohao.com/api/coin/coinrank?pagesize=100&webp=1"
	for coin_type in [0,1]:
		url = base_url+"&type="+str(coin_type)
		handurl(url,1)