####综合 币 k趋势
#
import numpy as np
import time
from rank_data import *

def run(time_type):
	if time_type == 'MIN':
		end_time = int(time.time())
		st_time = end_time-60
		sql = "select price from coin_price where second > '"+str(st_time)+"' and second < '"+str(end_time)+"' and type=1 order by second asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'M5':
		end_time = int(time.time())
		st_time = end_time-300
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'M15':
		end_time = int(time.time())
		st_time = end_time-15*60
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'M30':
		end_time = int(time.time())
		st_time = end_time-30*60
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'HOUR':
		end_time = int(time.time())
		st_time = end_time-60*60
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'H2':
		end_time = int(time.time())
		st_time = end_time-120*60
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'H4':
		end_time = int(time.time())
		st_time = end_time-4*60*60
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'H6':
		end_time = int(time.time())
		st_time = end_time-60*60*6
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'H12':
		end_time = int(time.time())
		st_time = end_time-60*60*12
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()
	if time_type == 'DAY':
		end_time = int(time.time())
		st_time = end_time-60*60*24
		sql = "select price from line_data_sp where from=1 and epochSecond > '"+str(st_time)+"' and epochSecond < '"+str(end_time)+"' order by epochSecond asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`,`price`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1,'"+str(price)+"')"
		print(sql)
		cursor.execute(sql)
		connect.commit()

		


if __name__ == '__main__':
	time_type = sys.argv[1] if len(sys.argv) >1 else 'MIN'
	connect = connect1()
	cursor = connect['cur']
	connect = connect['con']
	run(time_type)
