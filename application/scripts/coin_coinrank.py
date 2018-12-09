import requests
import pymysql.cursors
import sys
import time
import json

def run():
	handurl("1")

def handurl(curPage):
	global base_url
	global headers
	global connect
	url = base_url+"&page="+curPage
	rs = requests.get(url, headers=headers)
	if rs.status_code != 200:
		print(url+" 数据请求失败\n")
		return
	data = rs.json()
	records = data['data']
	for record in records:
		print(record)
	maxPageSize = data['maxpage']
	curPage = data['currpage']
	if int(curPage) <= int(maxPageSize):
		handurl(curPage)


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
	base_url = "https://dncapi.feixiaohao.com/api/coin/coinrank?type=0&pagesize=100&webp=1"
	connect = connect1()
	run()