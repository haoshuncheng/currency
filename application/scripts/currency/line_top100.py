#折线图数据脚本
import requests
from lxml import etree
import pymysql.cursors
import sys
import time

def main(time_type):
	sql = "select `name` from rank order by marketCap desc limit 0,100"
	cursor.execute(sql)
	rs = cursor.fetchall()
	rs = ["'"+x['name']+"'" for x in rs]
	# print(rs)
	# return
	# rs = 
	rs_str = "("+",".join(rs)+")"
	end_time = int(time.time())
	if time_type == 'MIN':
		st_time = end_time-60
	elif time_type == 'M5':
		st_time = end_time-60*5
		time_type2 = 'MIN'
	elif time_type == 'M15':
		st_time = end_time-60*15
		time_type2 = 'MIN'
	elif time_type == 'M30':
		st_time = end_time-60*30
		time_type2 = 'MIN'
	elif time_type == 'HOUR':
		st_time = end_time-60*60
		time_type2 = 'M5'
	elif time_type == 'H2':
		st_time = end_time-60*120
		time_type2 = 'M5'
	elif time_type == 'H4':
		st_time = end_time-60*240
		time_type2 = 'M5'
	elif time_type == 'H6':
		st_time = end_time-60*360
		time_type2 = 'M15'
	elif time_type == 'H12':
		st_time = end_time-60*720
		time_type2 = 'M30'
	elif time_type == 'DAY':
		st_time = end_time-60*1240
		time_type2 = 'HOUR'
	else:
		return
	if time_type == 'MIN':
		sql = "select avg(`high`) as high,avg(`low`) as low,avg(`open`) as open,avg(`close`) as close from line_data where `from` in "+rs_str+" and type='MIN' and epochSecond >= '"+str(st_time)+"' and epochSecond <= '"+str(end_time)+"'"
		print(sql)
		cursor.execute(sql)
		rs = cursor.fetchone()
		if not rs or not len(rs):
			return
		high,low,s_open,close = [rs[x] for x in rs]
	else:
		sql = "select `close` from line_data where `from` ='TOP100' and type='"+time_type2+"' and epochSecond >= '"+str(st_time)+"' and epochSecond <= '"+str(end_time)+"'"
		print(sql)
		cursor.execute(sql)
		rs = cursor.fetchall()
		if not rs or not len(rs):
			return
		record = [float(x['price']) for x in rs]
		s_open = record[0]
		close = record[-1]
		high = max(record)
		low = min(record)
	sql = "replace into line_data (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`to`) values('"+str(st_time)+"','"+time_type+"','"+str(high)+"','"+str(low)+"','"+str(s_open)+"','"+str(close)+"','TOP100','USD')"
	cursor.execute(sql)
	connect.commit()

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
	db = connect1()
	connect,cursor = [db[x] for x in db]
	if len(sys.argv) <= 1 or sys.argv[1] == '':
		print("脚本类型不可以为空\n")
	else:
		main(sys.argv[1])