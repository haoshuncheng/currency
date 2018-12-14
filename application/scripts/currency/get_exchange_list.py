#获取交易所列表
import requests
from lxml import etree
import sys
import time
import json
import re
from rank_data import *

def get_list(i):
	rs = get_requests("https://dncapi.feixiaohao.com/api/exchange/web-exchange?token=&page="+str(i)+"&pagesize=100&isinnovation=0&type=all&webp=1", 'json')
	if rs == False:
		print("list列表失败\n")
		return False
	if 'code' not in rs or rs['code']!='200' or 'data' not in rs or len(rs['data'])==0:
		print("json数据异常\n")
		return False



if __name__ == "__main__":
	for i in [1,2,3]:
		get_list(i)