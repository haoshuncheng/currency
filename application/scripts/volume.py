import requests
from lxml import etree
import pymysql.cursors
import sys
import time

def main():
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	connect = connect1()
	date = time.strftime("%Y-%m-%d", time.localtime())

	get_data(i, headers, connect, date)
	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

def get_data(i, headers, connect, date):
	rs = requests.get('https://www.feixiaohao.com.html', headers=headers)
	#rs = requests.get('https://www.feixiaohao.com/list_1.html', headers=headers)
	print(rs.status_code)
	if rs.status_code != 200:
		print("数据请求失败\n")
		return
	tree = etree.HTML(rs.text)
	r = tree.xpath('//table[@id="vol_exchange"]/tbody/tr')
	#r = tree.xpath('//table[@id="table"]//tr/td[2]/a/img/@alt')
	#print(r)
	for record in r:

		rank = record.xpath("./td[1]/span/text()")
		rank = rank[0] if len(rank) else 0
		href = record.xpath("./td[2]/a/@href")
		href = href[0] if len(href) else ''
		icon = record.xpath("./td[2]/a/img/@src")
		icon = icon[0] if len(icon) else ''
		name = record.xpath("./td[2]/a/text()")
		name = name[0] if len(name) else ''
		print([rank,href,icon,name])		

		# sql = "REPLACE INTO currency_data (rp_date,number,name,icon,market_cap_usd,market_cap_cny,market_cap_btc,price_usd,price_cny,num,volume_usd,volume_cny,volume_btc,text_red,char_line) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
		# data = (str(date),int(number),str(name),str(icon),str(market_cap_usd),str(market_cap_cny),str(market_cap_btc),str(price_usd),str(price_cny),str(num),str(volume_usd),str(volume_cny),str(volume_btc),str(text_red),str(char_line))
		# connect['cur'].execute(sql % data)
		# connect['con'].commit()
		# print('成功插入', connect['cur'].rowcount, '条数据')
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