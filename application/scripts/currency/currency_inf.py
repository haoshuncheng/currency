#货币详细信息
import requests
from lxml import etree
import pymysql.cursors
import sys
import time
import json
import re
from get_rank_list import *

def main():
	m_tr = get_rank_list()         #获取货币列表
	if m_tr == False:
		sys.exit()
	for res in m_tr:
		code = res['url'] if 'url' in res else ''
		url = "https://info.binance.com/cn/currencies/"+code
		print(url)
		line_data = get_requests(url)
		if line_data == False:
			print("无法获取详细数据\n")
			continue
		volume_value = get_data(line_data, '//div[@class="ix71fe-6 jgQppZ"]/ul/li[2]/div/text()')  				#24h成交量 全球 具体数值  
		volume_value = volume_value.split('(')[0] if volume_value!='' else ''
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
		rec = "('"+code+"','"+volume_value+"','"+web+"','"+web_url+"','"+browser+"','"+browser_url+"','"+white_paper+"','"+white_paper_url+"','"+sourceCode+"','"+sourceCodeUrl+"','"+community_url+"','"+str(maxSupply)+"','"+issue_date+"','"+issue_price+"','"+consensus+"','"+encryption+"','"+off_web+"','"+currency_type+"','"+inf+"')"
	
		get_pie_chart(code) #获取饼状图
		sql = "REPLACE INTO `currency_inf` (`code`,`volume_value`,`web`,`web_url`,`browser`,`browser_url`,`white_paper`,`white_paper_url`,`sourceCode`,`sourceCodeUrl`,`community_url`,`maxSupply`,`issue_date`,`issue_price`,`consensus`,`encryption`,`off_web`,`currency_type`,`inf`) VALUES "+rec
		connect['cur'].execute(sql)
		connect['con'].commit()
		print('成功插入', connect['cur'].rowcount, '条数据')

	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()


#获取饼状图
def get_pie_chart(code):
	print("获取饼状图数据\n")
	url = "https://dncapi.feixiaohao.com/api/coin/cointrades-web?code="+str(code)+"&webp=1"
	print(url)
	rs = get_requests(url, 'json')
	#print(rs)
	if rs == False or 'code' not in rs or rs['code']!='200' or 'data' not in rs or len(rs['data']) <= 0:
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