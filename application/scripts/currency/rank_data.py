#首页数据(货币排行榜)
import requests
from lxml import etree
import pymysql.cursors
import sys
import time
import json

def main():
	kline_data = get_kline_data()  #获取图形数据
	rs = get_requests("https://info.binance.com/cn/all")
	if rs == False:
		print("list列表失败\n")
		return

	print(rs)
	# abc = rs.xpath('//script[@nonce="3b1a756-24d45f8c-e046-4c99-ba71-74d0b5df61c5"]')
	# print(abc)

	# div_str=etree.tostring(abc[0],encoding='utf-8')
	# print(div_str)
	sys.exit()

	response = rs.xpath('//tbody[@class="s1apzr5v-2 ixZYaO"]/tr')
	if len(response) == 0:
		print("获取的货币列表为空\n")
		return
	data = ""
	for resp in response:
		order = get_data(resp, './td[1]/text()')
		pic = get_data(resp, './td[2]//img[@class="avatar"]/@src')
		name = get_data(resp, './td[2]//span[@class="abbr"]/text()')
		code = get_data(resp, './td[2]//span[@class="fullName"]/text()')
		price = get_data(resp, './td[3]//div[@class="s1oak5r5-0 hPVmeY"]/text()')		#价格
		updown = get_data(resp, './td[4]/div[@class="cw0nen-1 hUhTmi"]/text()')			#24h涨跌
		market = get_data(resp, './td[5]/span[@class="cqbzzs-0 kGbRkh"]/text()')  		#市值
		volume = get_data(resp, './td[7]/span[@class="cqbzzs-0 kGbRkh"]/text()')  		#24h成交量 全球
		circulation = get_data(resp, './td[8]/span[@class="cqbzzs-0 kGbRkh"]/text()')  	#流通数量
		kline = '' if kline_data==False or code.lower() not in kline_data else kline_data[code.lower()] #折线图
		url = "https://info.binance.com/cn/currencies/"+code.lower()
		print(url)
		line_data = get_requests(url)
		if line_data == False:
			print("无法获取详细数据\n")
			continue
		market_value = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[1]/div/text()')  				#市值 具体数值
		volume_value = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[2]/div/text()')  				#24h成交量 全球 具体数值  /////
		circulation_value = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[3]/div/text()')  		#流通数量 具体数值
		web = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[4]/div/a/text()')  					#web        /////
		web_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[4]/div/a/@href')  					#web url    ////
		browser = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[5]/div/a/text()')  				#浏览器     ////
		browser_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[5]/div/a/@href')  				#浏览器 url ////
		white_paper = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[6]/div/a/text()')  			#白皮书     ////
		white_paper_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[6]/div/a/@href')  			#白皮书 url /////
		sourceCode = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[7]/div/a/text()')  				#源代码     /////+++
		sourceCode_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[7]/div/a/@href')  			#源代码 url /////++
		community_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[8]//a/@href')  				#社区 url   /////
		max_to = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//tbody[1]/tr[2]/td[1]/text()')  		#最大供给量
		issue_date = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//tbody[1]/tr[2]/td[3]/text()')		#发行日期
		issue_price = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//tbody[1]/tr[2]/td[4]/text()')  	#发行价
		consensus = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//tbody[1]/tr[2]/td[5]/text()')  		#共识机制
		encryption = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//table[2]//tr[2]/td[2]/text()')  	#加密方式
		off_web = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//table[2]//tr[2]/td[5]/a/@href')  		#官网
		currency_type = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//table[2]//tr[2]/td[6]/text()')  #类型
		inf = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]/div[@class="s1qusdff-3 eCKrJW"]/p/text()') #简介
		res = "("+str(order)+",'"+pic+"','"+name+"','"+code+"','"+price+"','"+updown+"','"+market+"','"+volume+"','"+circulation+"','"+kline+"','"+market_value+"','"+volume_value+"','"+circulation_value+"','"+web+"','"+web_url+"','"+browser+"','"+browser_url+"','"+white_paper+"','"+white_paper_url+"','"+sourceCode+"','"+sourceCode_url+"','"+community_url+"','"+max_to+"','"+issue_date+"','"+issue_price+"','"+consensus+"','"+encryption+"','"+off_web+"','"+currency_type+"','"+inf+"')"
		data = res if data=="" else data+","+res
		get_pie_chart(code.lower(), code) #获取饼状图
		#insert(line_data) #储存数据

		# print([market_value,volume_value,circulation_value,web,web_url,browser,browser_url,white_paper,white_paper_url,sourceCode,sourceCode_url,community_url,max_to,issue_date,issue_price,consensus,encryption,off_web,currency_type,inf])
		# sys.exit()

	sql = "REPLACE INTO `rank` (`order`,`pic`,`name`,`code`,`price`,`updown`,`market`,`volume`,`circulation`,`kline`,`market_value`,`volume_value`,`circulation_value`,`web`,`web_url`,`browser`,`browser_url`,`white_paper`,`white_paper_url`,`sourceCode`,`sourceCode_url`,`community_url`,`max_to`,`issue_date`,`issue_price`,`consensus`,`encryption`,`off_web`,`currency_type`,`inf`) VALUES "+data
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

#获取饼状图
def get_pie_chart(code, code1):
	print("获取饼状图数据\n")
	url = "https://dncapi.feixiaohao.com/api/coin/cointrades-web?code="+str(code)+"&webp=1"
	print(url)
	rs = get_requests(url, 'json')
	#print(rs)
	if 'code' not in rs or rs['code']!='200' or 'data' not in rs or len(rs['data']) <= 0:
		print("饼状图接口返回数据异常或数据长度为0\n")
		return

	sql = "REPLACE INTO `pie_chart` (`code`,`data`) VALUES ('"+code1+"','"+json.dumps(rs['data'])+"')"
	connect['cur'].execute(sql)
	connect['con'].commit()
	print('成功插入', connect['cur'].rowcount, '条数据')

def get_data(response, rs):
	r = response.xpath(rs)
	return '' if len(r)==0 else trim(r[0])

#去除字符串两端空格 换行符 回车等
def trim(str):
	return str.strip()

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
	connect = connect1()
	main()