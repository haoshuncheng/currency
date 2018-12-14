#首页数据(货币排行榜)
import requests
from lxml import etree
import pymysql.cursors
import sys
import time
import json
import re
from get_rank_list import *

def main():
	kline_data = get_kline_data()  #获取图形数据
	m_tr = get_rank_list()         #获取货币列表
	if m_tr == False:
		sys.exit()
	data = ''
	for res in m_tr:
		if 'thumbUrl' in res and res['thumbUrl'] != '':
			pic = host_url+res['thumbUrl']
		elif 'imageUrl' in res and res['imageUrl'] != '':
			pic = host_url+res['imageUrl']
		else:
			pic = ''
		name = res['name'] if 'name' in res else ''
		code = res['url'] if 'url' in res else ''
		price = res['price'] if 'price' in res else 0 													#价格
		dayChange = res['dayChange'] if 'dayChange' in res else 0 										#24h涨跌
		marketCap = round(res['marketCap'], 2) if 'marketCap' in res and res['marketCap']!='' and res['marketCap']!=None else 0#市值
		volumeGlobal = res['volumeGlobal'] if 'volumeGlobal' in res else 0  							#24h成交量 全球
		circulatingSupply = res['circulatingSupply'] if 'circulatingSupply' in res else 0  				#流通数量
		kline = '' if kline_data==False or code not in kline_data else kline_data[code] 				#折线图
		rec = "('"+pic+"','"+name+"','"+code+"','"+str(price)+"','"+str(dayChange)+"',"+str(marketCap)+",'"+str(volumeGlobal)+"','"+str(circulatingSupply)+"','"+kline+"')"
		data = ","+rec if data!='' else rec
	sql = "REPLACE INTO `rank` (`pic`,`name`,`code`,`price`,`dayChange`,`marketCap`,`volumeGlobal`,`circulatingSupply`,`kline`) VALUES "+data
	connect['cur'].execute(sql)
	connect['con'].commit()
	print('成功插入', connect['cur'].rowcount, '条数据')

	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

#获取图形数据
def get_kline_data():
	connect['cur'].execute("select `code`,`kline_data` from `fxh_rank`")
	if connect['cur'].rowcount == 0:
		print("fxh_rank表里无数据\n")
		return False
	rs = {}
	for row in connect['cur'].fetchall():
		rs[row['code']] = row['kline_data']
	return rs



#发送请求
def get_requests(url, dattype=''):
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	try:
		rs = requests.get(url, headers=headers)
		if rs.status_code != 200:
			print("数据请求失败\n")
			return False
		if dattype=='json':
			return rs.json()
		elif dattype=='text':
			return rs.text
		return etree.HTML(rs.text)
	except:
		return False

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

if __name__ == "__main__":
	host_url = 'https://resource.bnbstatic.com/'
	connect = connect1()
	main()