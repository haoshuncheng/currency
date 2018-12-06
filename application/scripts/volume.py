import requests
from lxml import etree
import pymysql.cursors
import sys
import time
from common import *
def main():
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	connect = connect1()
	date = time.strftime("%Y-%m-%d", time.localtime())
	for d_type in ['vol_exchange','vol_coin']:
		get_data(headers, connect, d_type)
	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

def get_data(headers, connect, d_type):
	rs = requests.get('https://www.feixiaohao.com', headers=headers)
	#rs = requests.get('https://www.feixiaohao.com/list_1.html', headers=headers)
	print(rs.status_code)
	if rs.status_code != 200:
		print("数据请求失败\n")
		return
	tree = etree.HTML(rs.text)
	r = tree.xpath('//table[@id="'+d_type+'"]/tbody/tr')
	for record in r:
		rank = record.xpath("./td[1]/span/text()")
		rank = rank[0] if len(rank) else 0
		href = record.xpath("./td[2]/a/@href")
		href = href[0] if len(href) else ''
		icon = record.xpath("./td[2]/a/img/@src")
		icon = icon[0] if len(icon) else ''
		name = record.xpath("./td[2]/a/text()")
		name = name[1] if len(name) else ''
		price = record.xpath("./td[3]/text()")
		price = price[0] if len(price) else ''
		data_type = d_type
		rp_date = getTime(0,'-')
		#print([rank,href,icon,name,price])		

		sql = "REPLACE INTO volume (rp_date,name,icon,rank,data_type,href,price) VALUES ('"+rp_date+"','"+name+"','"+icon+"',"+rank+",'"+data_type+"','"+href+"','"+price+"')"
		# sql = "REPLACE INTO volume (rp_date,name,icon,rank,data_type,href,price) VALUES ('%s','%s',%s,'%s','%s','%s','%s')"
		# data = (rp_date,name,icon,rank,data_type,href,price)
		#connect['cur'].execute(sql % data)
		connect['cur'].execute(sql)
		connect['con'].commit()
		print('成功插入', connect['cur'].rowcount, '条数据')
		#print(alt)
	#print(len(r))

	# r = tree.xpath('//tr[@id="bitcoin"]/td[@class="change"]/span/@class')
	# print(r)

	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

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

if __name__ == "__main__":
	main()