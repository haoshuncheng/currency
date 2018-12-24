####综合 币 k趋势
#
import numpy as np
import time
from rank_data import *

def run(time_type):
	if time_type == 'MIN':
		end_time = int(time.time())
		st_time = end_time-60
		sql = "select price from coin_price where second > '"+str(st_time)+"' and second < '"+str(end_time)+"' order by second asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [float(x['price']) for x in rs]
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		sql = "replace into line_data_sp (`epochSecond`,`type`,`high`,`low`,`open`,`close`,`from`) values('"+str(st_time)+"','"+time_type+"','"+str(mx)+"','"+str(mn)+"','"+str(st)+"','"+str(end)+"',1)"
		print(sql)
		cursor.execute(sql)
		connect.commit()
		
		


if __name__ == '__main__':
	time_type = sys.argv[1] if len(sys.argv) >1 else 'MIN'
	connect = connect1()
	cursor = connect['cur']
	connect = connect['con']
	run(time_type)
