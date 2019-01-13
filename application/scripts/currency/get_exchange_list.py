#获取交易所列表
import requests
from lxml import etree
import sys
import time
import json
import re
import html
from rank_data import *

def get_list(url,isinnovation):
	print(url)

	rs = get_requests(url, 'json')
	if rs == False:
		print("list列表失败\n")
		return False
	if 'code' not in rs or str(rs['code'])!='200' or 'data' not in rs or len(rs['data'])==0:
		print(url+"asasasasasa")
		print("json数据异常\n")
		return False
	for record in rs['data']:
		try:
			# record['isinnovation'] = isinnovation
			# record['labels_id'] = 0 if not record['labels_id'] else record['labels_id']
			# record['isfocus'] = 0 if not record['isfocus'] else 1
			# del record['desc']
			# record['isshare'] = 0 if not record['isshare'] else 1
			# write(connect['con'],'exchange',record)
			# exchangeTrades_url = "https://dncapi.feixiaohao.com/api/exchange/exchangetrades?code="+record['id']+"&webp=1"
			# print(exchangeTrades_url)
			# exchange_rs = get_requests(exchangeTrades_url, 'json')
			# if exchange_rs == False:
			# 	print("list列表失败\n")
			# 	continue
			# if 'code' not in exchange_rs or str(exchange_rs['code'])!='200' or 'data' not in exchange_rs or len(exchange_rs['data'])==0:
			# 	print(exchangeTrades_url)
			# 	print("json数据异常\n")
			# 	continue
			# exchangetrades_data = json.dumps(exchange_rs['data'])
			# cursor = connect['cur']
			# cursor.execute("REPLACE INTO exchangetrades(code,info) values('"+record['id']+"','"+exchangetrades_data+"')")
			# connect['con'].commit()

			# coin_pairs_url = "https://dncapi.feixiaohao.com/api/exchange/coinpair_list"
			# print(coin_pairs_url)
			# data = {"code":record['id'],"page":1,"pagesize":1000,"webp":1}
			# coin_pairs_rs = post_requests(coin_pairs_url,json.dumps(data))
			# if coin_pairs_rs == False:
			# 	print("list列表失败\n")
			# 	continue
			# if 'code' not in coin_pairs_rs or str(coin_pairs_rs['code'])!='200' or 'data' not in coin_pairs_rs or len(coin_pairs_rs['data'])==0:
			# 	print(data)
			# 	print("json数据异常\n")
			# 	continue
			# coin_pairs_data = coin_pairs_rs['data']
			# for coin_record in coin_pairs_data:
			# 	coin_record['code'] = record['id']
			# 	write(connect['con'],'coin_pairs',coin_record)

			# exchangeinfo_url = "https://dncapi.feixiaohao.com/api/exchange/exchangeinfo?code="+record['id']+"&webp=1"
			# exchangeinfo = get_requests(exchangeinfo_url, 'json')
			# if exchangeinfo == False:
			# 	print("list列表失败\n")
			# 	continue
			# if 'code' not in exchangeinfo or str(exchangeinfo['code'])!='200' or 'data' not in exchangeinfo or len(exchangeinfo['data'])==0:
			# 	print(exchangeinfo_url)
			# 	print("json数据异常\n")
			# 	continue
			# exchangeinfo = exchangeinfo['data']
			# exchangeinfo['description'] = html.escape(exchangeinfo['desc'])
			# del exchangeinfo['desc']
			# write(connect['con'],'exchangeinfo',exchangeinfo)
			
			exchangescore_url = "https://mifengcha.com/exchange/"+record['id']
			print(exchangescore_url)
			rs = requests.get(exchangescore_url)
			text =rs.text
			# print(text)
			content = re.findall(r"<script>window.__NUXT__=(.*);</script>",text)
			t = content[0]
			params = re.findall(r"^\(function\((.*)\)\{return",t)
			params = params[0].split(",")
			params2 = re.findall(r"\}\}\((.*)\)\)$",t)
			params2 = params2[0].split(",")
			score = re.findall(r"score\:\{(.*)\}\,Currencies",t)
			score ={r.split(":")[0]:r.split(":")[1]  for r in  score[0].split(",")}

			for k,y in score.items():
				if y in params:
					score[k] = params2[params.index(y)].replace('"','')
				else:
					score[k] = y.replace('"','')
			print(score)
			cursor = connect['cur']
			cursor.execute("REPLACE INTO exchangescore(code,info) values('"+record['id']+"','"+json.dumps(score)+"')")
			connect['con'].commit()

			pairData = re.findall(r"pairData\:\[(.*)\]\,basePairData",t)
			pairData = [r for r in pairData[0].split("},")]
			tt = []
			for rec in pairData:
				rec = {r.split(":")[0].replace("{",""):r.split(":")[1].replace("}","") for r in rec.split(",")}
				for k,y in rec.items():
					if y in params:
						rec[k] = params2[params.index(y)].replace('"','')
					else:
						rec[k] = y.replace('"','')
				tt.append(rec)
			print(tt)
			cursor = connect['cur']
			cursor.execute("REPLACE INTO exchangepairdata(code,info) values('"+record['id']+"','"+json.dumps(tt)+"')")
			connect['con'].commit()
			# print(tt)


			basepairData = re.findall(r"basePairData\:\[(.*)\]\,hasKline",t)
			basepairData = [r for r in basepairData[0].split("},")]
			tt = []
			for rec in basepairData:
				rec = {r.split(":")[0].replace("{",""):r.split(":")[1].replace("}","") for r in rec.split(",")}
				for k,y in rec.items():
					if y in params:
						rec[k] = params2[params.index(y)].replace('"','')
					else:
						rec[k] = y.replace('"','')
				tt.append(rec)
			print(tt)
			cursor = connect['cur']
			cursor.execute("REPLACE INTO exchangebasepairdata(code,info) values('"+record['id']+"','"+json.dumps(tt)+"')")
			connect['con'].commit()
			# print(tt)
			


		except:
			s=sys.exc_info()
			print ("Error '%s' happened on line %d" % (s[1],s[2].tb_lineno))

if __name__ == "__main__":
	connect = connect1()
	for isinnovation in [0,1]:
		for page in range(1,11):
			url = "https://dncapi.feixiaohao.com/api/exchange/web-exchange?pagesize=100&type=all&webp=1"+"&isinnovation="+str(isinnovation)+"&page="+str(page)
			get_list(url,isinnovation)
