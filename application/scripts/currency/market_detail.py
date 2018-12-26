import requests
from lxml import etree
import pymysql.cursors
import sys
import time

def main():
	url = "https://api.huobipro.com/market/detail?symbol=hb10usdt"
	rs = get_requests(url,"json")
	ts = rs['ts']
	tick = rs['tick']
	amount = tick['amount']
	s_open = tick['open']
	close = tick['close']
	high = tick['high']
	low = tick['low']
	count = tick['count']
	vol = tick['vol']
	coin = 'HB10'
	sql = "replace into market_detail (ts,amount,open,close,high,low,count,vol,coin) values('"+str(ts)+"','"+str(amount)+"','"+str(s_open)+"','"+str(close)+"','"+str(high)+"','"+str(low)+"','"+str(count)+"','"+str(vol)+"','"+str(coin)+"')"
	cursor.execute(sql)
	connect.commit()

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
	
	db = connect1()
	connect,cursor = [db[x] for x in db]
	main()