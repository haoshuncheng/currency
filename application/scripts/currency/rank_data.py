#首页数据(货币排行榜)
import requests
from lxml import etree
import pymysql.cursors
import sys
import time
import json
import re

def main():
	kline_data = get_kline_data()  #获取图形数据
	rs = get_requests("https://info.binance.com/cn/all", 'text')
	if rs == False:
		print("list列表失败\n")
		return
	m_tr =  re.findall(r'"initialState":(.*?),"initialProps"', rs, re.S|re.M)
	if len(m_tr) == 0:
		print("正则匹配数据失败\n")
		sys.exit()
	m_tr = json.loads(m_tr[0])
	if 'coinList' not in m_tr:
		print("数据中不含coinList\n")
		sys.exit()
	for res in m_tr['coinList']:
		pic = host_url+res['thumbUrl'] if 'thumbUrl' in res else ''
		name = res['name'] if 'name' in res else ''
		code = res['url'] if 'url' in res else ''
		price = res['price'] if 'price' in res else 0 													#价格
		dayChange = res['dayChange'] if 'dayChange' in res else 0 										#24h涨跌
		marketCap = res['marketCap'] if 'marketCap' in res else 0   									#市值
		volumeGlobal = res['volumeGlobal'] if 'volumeGlobal' in res else 0  							#24h成交量 全球
		circulatingSupply = res['circulatingSupply'] if 'circulatingSupply' in res else 0  				#流通数量
		kline = '' if kline_data==False or code not in kline_data else kline_data[code] 				#折线图
		url = "https://info.binance.com/cn/currencies/"+code
		print(url)
		line_data = get_requests(url)
		if line_data == False:
			print("无法获取详细数据\n")
			continue
		volume_value = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[2]/div/text()')  				#24h成交量 全球 具体数值  
		web = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[4]/div/a/text()')  					#web        
		web_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[4]/div/a/@href')  					#web url    
		browser = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[5]/div/a/text()')  				#浏览器     
		browser_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[5]/div/a/@href')  				#浏览器 url 
		white_paper = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[6]/div/a/text()')  			#白皮书     
		white_paper_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[6]/div/a/@href')  			#白皮书 url 
		sourceCode = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[7]/div/a/text()')  				#源代码     
		sourceCodeUrl = res['sourceCodeUrl'] if 'sourceCodeUrl' in res else '' 									#源代码 url 
		community_url = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[8]//a/@href')  				#社区 url   
		maxSupply = res['maxSupply'] if 'maxSupply' in res else 0  												#最大供给量
		issue_date = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//tbody[1]/tr[2]/td[3]/text()')		#发行日期
		issue_price = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//tbody[1]/tr[2]/td[4]/text()')  	#发行价
		consensus = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//tbody[1]/tr[2]/td[5]/text()')  		#共识机制
		encryption = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//table[2]//tr[2]/td[2]/text()')  	#加密方式
		off_web = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//table[2]//tr[2]/td[5]/a/@href')  		#官网
		currency_type = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]//table[2]//tr[2]/td[6]/text()')  #类型
		inf = get_data(line_data, '//div[@class="s1qusdff-0 fRRtWs"]/div[@class="s1qusdff-3 eCKrJW"]/p/text()') #简介
		res = "('"+pic+"','"+name+"','"+code+"','"+str(price)+"',"+str(dayChange)+",'"+str(marketCap)+"','"+str(volumeGlobal)+"','"+str(circulatingSupply)+"','"+kline+"','"+volume_value+"','"+web+"','"+web_url+"','"+browser+"','"+browser_url+"','"+white_paper+"','"+white_paper_url+"','"+sourceCode+"','"+sourceCodeUrl+"','"+community_url+"','"+str(maxSupply)+"','"+issue_date+"','"+issue_price+"','"+consensus+"','"+encryption+"','"+off_web+"','"+currency_type+"','"+inf+"')"
	
		get_pie_chart(code) #获取饼状图
		sql = "REPLACE INTO `rank` (`pic`,`name`,`code`,`price`,`dayChange`,`marketCap`,`volumeGlobal`,`circulatingSupply`,`kline`,`volume_value`,`web`,`web_url`,`browser`,`browser_url`,`white_paper`,`white_paper_url`,`sourceCode`,`sourceCodeUrl`,`community_url`,`maxSupply`,`issue_date`,`issue_price`,`consensus`,`encryption`,`off_web`,`currency_type`,`inf`) VALUES "+res
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
def get_pie_chart(code):
	print("获取饼状图数据\n")
	url = "https://dncapi.feixiaohao.com/api/coin/cointrades-web?code="+str(code)+"&webp=1"
	print(url)
	rs = get_requests(url, 'json')
	#print(rs)
	if 'code' not in rs or rs['code']!='200' or 'data' not in rs or len(rs['data']) <= 0:
		print("饼状图接口返回数据异常或数据长度为0\n")
		return

	sql = "REPLACE INTO `pie_chart` (`code`,`data`) VALUES ('"+code+"','"+json.dumps(rs['data'])+"')"
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
	elif dattype=='text':
		return rs.text
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
	host_url = 'https://resource.bnbstatic.com/'
	connect = connect1()
	main()