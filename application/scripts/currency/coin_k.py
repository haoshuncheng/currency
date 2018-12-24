####综合 币 k趋势
#
import numpy as np
import time
from rank_data import *

def run(time_type):
	if time_type == '1m':
		end_time = int(time.time())
		st_time = end_time-600
		sql = "select price from coin_price where second > '"+str(st_time)+"' and second < '"+str(end_time)+"' order by second asc"
		cursor.execute(sql)
		rs = cursor.fetchall()
		record = [x['price'] for x in rs]
		print(record)
		st = record[0]
		end = record[-1]
		mx = max(record)
		mn = min(record)
		price = np.mean(record)
		print([st,end,mx,mn,price])


if __name__ == '__main__':
	time_type = sys.argv[1] if len(sys.argv) >1 else '1m'
	connect = connect1()
	cursor = connect['cur']
	connect = connect['con']
	run(time_type)
