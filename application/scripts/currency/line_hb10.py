#折线图数据脚本
import requests
from lxml import etree
import pymysql.cursors
import sys
import time
def main(time_type):
	if time_type not in time_types:
		return
	time_type = time_types[time_type]
	url = "https://api.huobipro.com/market/history/kline?size=200&symbol=hb10usdt&period="+time_type
	rs = get_requests(url,'json')
	print(rs)

def connect1():
	connect = pymysql.Connect(
		host='116.62.118.136',
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

#发送请求
def get_requests(url, dattype=''):
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	rs = requests.get(url, headers=headers)
	if rs.status_code != 200:
		print("数据请求失败\n")
		return False
	if dattype=='json':
		return rs.json()
	return etree.HTML(rs.text)

if __name__ == "__main__":
	time_types = {"MIN":'1min', 'M5':'5min', 'M15':'15min', 'M30':'30min','HOUR':'60min','DAY':'1day','H12':"60min",'H6':"60min",'H4':"60min",'H2':"60min"}
	db = connect1()
	connect,cursor = [db[x] for x in db]
	if len(sys.argv) <= 1 or sys.argv[1] == '':
		print("脚本类型不可以为空\n")
	else:
		main(sys.argv[1])