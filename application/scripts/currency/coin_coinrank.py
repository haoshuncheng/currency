#fxh货币数据
import requests
import pymysql.cursors
import sys
import time
import json

def handurl(url,curPage,coin_type):

	global headers
	global connect
	full_url = url+str(coin_type)+"&page="+str(curPage)
	rs = requests.get(full_url, headers=headers)
	if rs.status_code != 200:
		print(full_url+" 数据请求失败\n")
		return
	else:
		print(full_url+" 数据请求成功\n")
	data = rs.json()
	records = data['data']
	for record in records:
		# sql = "replace into coin_rank(current_price,current_price_usd,update_time,code,name,fullname,logo,market,platform,platform_name,change_percent,market_value,vol,supply,star_level,kline_data,market_value_usd,vol_usd,marketcap,high_price,drop_ath,low_price,high_time,low_time,isifo,ismineable,logo_small,coin_type) values(%s,%s,'%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,'%s',%s,%s,%s,%s,%s,%s,'%s','%s',%s,%s,'%s',%s)"
		# vs = (handleStr(record['current_price']),handleStr(record['current_price_usd']),handleStr(record['update_time']),handleStr(record['code']),handleStr(record['name']),handleStr(record['fullname']),handleStr(record['logo']),handleStr(record['market']),handleStr(record['platform']),handleStr(record['platform_name']),handleStr(record['change_percent']),handleStr(record['market_value']),handleStr(record['vol']),handleStr(record['supply']),handleStr(record['star_level']),handleStr(record['kline_data']),handleStr(record['market_value_usd']),handleStr(record['vol_usd']),handleStr(record['marketcap']),handleStr(record['high_price']),handleStr(record['drop_ath']),handleStr(record['low_price']),handleStr(record['high_time']),handleStr(record['low_time']),handleStr(record['isifo']),handleStr(record['ismineable']),handleStr(record['logo_small']),coin_type)
		sql = "replace into fxh_rank(code,name,kline_data) values('%s','%s','%s')"
		vs = (handleStr(record['code']),handleStr(record['name']),handleStr(record['kline_data']))
		connect['cur'].execute(sql % vs)
		connect['con'].commit()
	maxPageSize = data['maxpage']
	curPage = data['currpage']+1
	if int(curPage) <= int(maxPageSize):
		handurl(url,curPage,coin_type)

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