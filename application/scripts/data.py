import requests
from lxml import etree
import pymysql.cursors

def main():
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	connect = connect1()
	for i in range(1, 26):
		get_data(i, headers, connect)
	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

def get_data(i, headers, connect):
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
		name = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[2]/a/img/@alt')[0]
		#市值
		market_cap_usd = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[3]/@data-usd')[0]
		market_cap_cny = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[3]/@data-cny')[0]
		market_cap_btc = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[3]/@data-btc')[0]
		#价格
		price_usd = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[4]/a/@data-usd')[0]
		price_cny = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[4]/a/@data-cny')[0]
		#流通数量
		num = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[5]/text()')[0]
		#成交额
		volume_usd = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[6]/a/@data-usd')[0]
		volume_cny = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[6]/a/@data-cny')[0]
		volume_btc = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[6]/a/@data-btc')[0]
		#涨幅
		text_red = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[7]/span/text()')[0]
		#价格趋势
		char_line = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[8]/span/text()')[0]
		# char_polygon = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[8]/svg[@class="peity"]/polygon/@points')
		# char_polyline = tree.xpath('//table[@id="table"]//tr['+str(k)+']/td[8]/svg/polyline/@points')
		# print(char_polygon)
		# print(char_polyline)

		sql = "REPLACE INTO currency_data (name,icon,market_cap_usd,market_cap_cny,market_cap_btc,price_usd,price_cny,num,volume_usd,volume_cny,volume_btc,text_red,char_line) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
		data = (name,icon,market_cap_usd,market_cap_cny,market_cap_btc,price_usd,price_cny,num,volume_usd,volume_cny,volume_btc,text_red,char_line)
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