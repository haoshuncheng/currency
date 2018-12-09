import requests
import pymysql.cursors
import sys
import time
import json

def run():
	
	base_url = "https://dncapi.feixiaohao.com/api/coin/coinrank?page=1&type=0&pagesize=100&webp=1"
	handurl(base_url)

def handurl(url):
	global headers
	global connect

	rs = requests.get(url, headers=headers)
	if rs.status_code != 200:
		print(url+" 数据请求失败\n")
		return
	records = rs.json()
	for record in records:
		print(record)
		time.sleep(3)


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
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	connect = connect1()
	run()