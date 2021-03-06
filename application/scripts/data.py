#弃用
import requests
from lxml import etree
import pymysql.cursors
import sys
import time

def main():
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	connect = connect1()
	date = time.strftime("%Y-%m-%d", time.localtime())
	for i in range(1, 26):
		print("获取："+str(i)+"页数据")
		get_data(i, headers, connect, date)
	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

def get_data(i, headers, connect, date):
	rs = requests.get('https://www.feixiaohao.com/list_'+str(i)+'.html', headers=headers)
	#rs = requests.get('https://www.feixiaohao.com/list_1.html', headers=headers)
	print(rs.status_code)
	if rs.status_code != 200:
		print("数据请求失败\n")
		return
	tree = etree.HTML(rs.text)
	r = tree.xpath('//table[@id="table"]//tr')
	#r = tree.xpath('//table[@id="table"]//tr/td[2]/a/img/@alt')
	#print(r)
	for k in range(1, len(r)):
		img = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[2]/a/img/@src')
		if len(img) == 0 or img[0] == "":
			continue
		icon = 'https:'+img[0]
		#名称
		name = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[2]/a/img/@alt')
		if len(name) == 0 or name[0] == "":
			continue
		name = name[0]
		print(name)

		number = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[1]/text()')
		if len(number) == 0 or number[0] == "":
			continue
		number = number[0]
		#市值
		market_cap_usd = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[3]/@data-usd')
		market_cap_usd = market_cap_usd[0] if len(market_cap_usd)>=1 else ''
		market_cap_cny = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[3]/@data-cny')
		market_cap_cny = market_cap_cny[0] if len(market_cap_cny)>=1 else ''
		market_cap_btc = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[3]/@data-btc')
		market_cap_btc = market_cap_btc[0] if len(market_cap_btc)>=1 else ''
		market_cap_show = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[3]/text()')
		market_cap_show = market_cap_show[0] if len(market_cap_show)>=1 else ''
		#价格
		price_usd = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[4]/a/@data-usd')
		price_usd = price_usd[0] if len(price_usd)>=1 else ''
		price_cny = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[4]/a/@data-cny')
		price_cny = price_cny[0] if len(price_cny)>=1 else ''
		price_show = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[4]/a/text()')
		price_show = price_show[0] if len(price_show)>=1 else ''
		#流通数量
		num = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[5]/text()')
		if len(num) <= 0:
			num = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[5]/a/text()')
		num = num[0] if len(num)>=1 else ''
		#成交额
		volume_usd = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[6]/a/@data-usd')
		volume_usd = volume_usd[0] if len(volume_usd)>=1 else ''
		volume_cny = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[6]/a/@data-cny')
		volume_cny = volume_cny[0] if len(volume_cny)>=1 else ''
		volume_btc = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[6]/a/@data-btc')
		volume_btc = volume_btc[0] if len(volume_btc)>=1 else ''
		volume_show = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[6]/a/text()')
		volume_show = volume_show[0] if len(volume_show)>=1 else ''
		#涨幅
		text_red = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[7]/span/text()')
		text_red = text_red[0] if len(text_red)>=1 else ''
		#价格趋势
		char_line = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[8]/span/text()')
		char_line = char_line[0] if len(char_line)>=1 else ''
		# char_polygon = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[8]/svg[@class="peity"]/polygon/@points')
		# char_polyline = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[8]/svg/polyline/@points')
		# print(char_polygon)
		# print(char_polyline)

		sql = "REPLACE INTO currency_data (volume_show,price_show,market_cap_show,rp_date,number,name,icon,market_cap_usd,market_cap_cny,market_cap_btc,price_usd,price_cny,num,volume_usd,volume_cny,volume_btc,text_red,char_line) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
		data = (str(volume_show),str(price_show),str(market_cap_show),str(date),int(number),str(name),str(icon),str(market_cap_usd),str(market_cap_cny),str(market_cap_btc),str(price_usd),str(price_cny),str(num),str(volume_usd),str(volume_cny),str(volume_btc),str(text_red),str(char_line))
		print(data)
		connect['cur'].execute(sql % data)
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