#获取货币列表
import requests
from lxml import etree
import sys
import time
import json
import re
from rank_data import *

#获取所有货币
def get_rank_list():
	rs = get_requests("https://info.binance.com/cn/all", 'text')
	if rs == False:
		print("list列表失败\n")
		return False
	m_tr =  re.findall(r'"initialState":(.*?),"initialProps"', rs, re.S|re.M)
	if len(m_tr) == 0:
		print("正则匹配数据失败\n")
		return False
	m_tr = json.loads(m_tr[0])
	return m_tr