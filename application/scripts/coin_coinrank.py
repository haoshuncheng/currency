import requests
import pymysql.cursors
import sys
import time
import json

def handurl(url,curPage,coin_type):

	global headers
	global connect
	full_url = url+str(coin_type)+"&page="+str(curPage)
	print(full_url)
	rs = requests.get(full_url, headers=headers)
	if rs.status_code != 200:
		print(full_url+" 数据请求失败\n")
		return
	data = rs.json()
	records = data['data']
	for record in records:
		sql = "replace into coin_rank(current_price,current_price_usd,update_time,code,name,fullname,logo,market,platform,platform_name,change_percent,market_value,vol,supply,star_level,kline_data,market_value_usd,vol_usd,marketcap,high_price,drop_ath,low_price,high_time,low_time,isifo,ismineable,logo_small,coin_type) values(%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,'%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,'%s',%s)"

		vs = (handStr(record['current_price']),handStr(record['current_price_usd']),handStr(record['update_time']),handStr(record['code']),handStr(record['name']),handStr(record['fullname']),handStr(record['logo']),handStr(record['market']),handStr(record['platform']),handStr(record['platform_name']),handStr(record['change_percent']),handStr(record['market_value']),handStr(record['vol']),handStr(record['supply']),handStr(record['star_level']),handStr(record['kline_data']),handStr(record['market_value_usd']),handStr(record['vol_usd']),handStr(record['marketcap']),handStr(record['high_price']),handStr(record['drop_ath']),handStr(record['low_price']),handStr(record['high_time']),handStr(record['low_time']),handStr(record['isifo']),handStr(record['ismineable']),handStr(record['logo_small']),coin_type)
		connect['cur'].execute(sql % vs)
		connect['con'].commit()
	maxPageSize = data['maxpage']
	curPage = data['currpage']+1
	if int(curPage) <= int(maxPageSize):
		handurl(url,curPage,coin_type)

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

def handleStr(str_t):
	if isinstance (str_t,str):
		return str_t.replace("'","''")
	return str_t
if __name__ == '__main__':
	connect = connect1()
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	base_url = "https://dncapi.feixiaohao.com/api/coin/coinrank?pagesize=100&webp=1"
	for coin_type in [0,1]:
		url = base_url+"&type="
		handurl(url,1,coin_type)