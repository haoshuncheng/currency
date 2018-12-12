#折线图数据脚本
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
	#print(rs)
	if 'code' not in rs or rs['code']!=0 or 'result' not in rs or 'total' not in rs['result'] or rs['result']['total']==0 or 'data' not in rs['result']:
		print("接口返回数据异常或数据长度为0\n")
		return
	data = ""
	print(len(rs['result']['data']))
	for v in rs['result']['data']:
		epochSecond = v['epochSecond'] if 'epochSecond' in v else ''
		type1 = v['type'] if 'type' in v else ''
		from1 = v['from'] if 'from' in v else ''
		to = v['to'] if 'to' in v else ''
		high = float(v['high']) if 'high' in v else ''
		low = float(v['low']) if 'low' in v else ''
		open1 = float(v['open']) if 'open' in v else ''
		close = float(v['close']) if 'close' in v else ''
		volumeFrom = float(v['volumeFrom']) if 'volumeFrom' in v else ''
		volumeTo = float(v['volumeTo']) if 'volumeTo' in v else ''
		res = "('"+str(epochSecond)+"','"+str(type1)+"','"+str(from1)+"','"+str(to)+"',"+str(high)+","+str(low)+","+str(open1)+","+str(close)+","+str(volumeFrom)+","+str(volumeTo)+")"
		data = res if data=="" else data+","+res
	sql = "REPLACE INTO `line_data` (`epochSecond`,`type`,`from`,`to`,`high`,`low`,`open`,`close`,`volumeFrom`,`volumeTo`) VALUES "+data
	connect['cur'].execute(sql)
	connect['con'].commit()
	print('成功插入', connect['cur'].rowcount, '条数据')

#获取时间范围
def get_range_time(script_type):
	if end != 0:
		time2 = int(end)
	else:
		time2 = int(time.time())
	if start != 0:
		time1 = start
	elif script_type == 'MIN':
		time1 = time2 - 600
	elif script_type in ['M15','M5']:
		time1 = time2 - 3600
	elif script_type in ['HOUR','M30']:
		time1 = time2 - 3600*2
	elif script_type in ['H6','H4','H2']:
		time1 = time2 - 3600*24
	else:
		time1 = time2 - 3600*24*2
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
	start = 0
	end = 0
	if len(sys.argv) <= 1 or sys.argv[1] == '':
		print("脚本类型不可以为空\n")
	else:
		if len(sys.argv) >= 3:
			start = sys.argv[2]
		if len(sys.argv) >= 4:
			end = sys.argv[3]	
		connect = connect1()
		main(sys.argv[1])