import requests
from lxml import etree
import pymysql.cursors
import sys
import time

def main(script_type):
	script_types = ['DAY','H12','H6','H4','H2','HOUR','M30','M15','M5','MIN']
	if script_type not in script_types:
		print("脚本类型不正确\n")
		return
	rs = get_requests("https://info.binance.com/en/all")
	if rs == False:
		print("获取货币列表失败\n")
		return
	currency_name = rs.xpath('//span[@class="abbr"]/text()')
	if len(currency_name) == 0:
		print("获取的货币列表为空\n")
		return
	time = get_range_time(script_type)  #获取时间范围
	for name in currency_name:
		url = "https://www.binance.com/info-api/v1/public/agg_kline?base="+name+"&quote=USD&type="+script_type+"&limit=2000&startEpochSecond="+str(time[0])+"&endEpochSecond="+str(time[1])
		print(url)
		line_data = get_requests(url, 'json')
		if line_data == False:
			print("无法获取数据，执行下一货币\n")
			continue
		insert(line_data) #储存数据




	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

#储存数据
def insert(rs):
	print(rs)
	if 'code' not in rs or rs['code']!=0 or 'result' not in rs or 'total' not in rs['result'] or rs['result']['total']==0 or 'data' not in rs['result']:
		print("接口返回数据异常或数据长度为0\n")
		return
	data = ""
	print(len(rs['result']['data']))
	for v in rs['result']['data']:
		res = "('"+str(v['epochSecond'])+"','"+str(v['type'])+"','"+str(v['from'])+"','"+str(v['to'])+"',"+str(v['high'])+","+str(v['low'])+","+str(v['open'])+","+str(v['close'])+","+str(v['volumeFrom'])+","+str(v['volumeTo'])+")"
		data = res if data=="" else data+","+res


	sql = "REPLACE INTO `line_data` (`epochSecond`,`type`,`from`,`to`,`high`,`low`,`open`,`close`,`volumeFrom`,`volumeTo`) VALUES "+data
	connect['cur'].execute(sql)
	connect['con'].commit()
	print('成功插入', connect['cur'].rowcount, '条数据')

#获取时间范围
def get_range_time(script_type):
	time2 = int(time.time())
	if script_type in ['M15','M5','MIN']:
		time1 = time2 - 3600*24
	else:
		time1 = time2 - 3600*24*5
	return [time1, time2]



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
	if len(sys.argv) <= 1 or sys.argv[1] == '':
		print("脚本类型不可以为空\n")
	else:
		connect = connect1()
		main(sys.argv[1])