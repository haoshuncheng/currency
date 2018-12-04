import requests
from lxml import etree
import pymysql.cursors
import sys
import datetime
def main():
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	connect = connect1()
	for i in range(1,3):
		for j in range(1,4):
			for c_type in ['up','down']:
				get_data(i, j, c_type, headers, connect)
def getTime(days = 1,DateSplit=None):
    if not DateSplit:
        Datetype = "%Y%m%d"
    else:
        Datetype = "%Y"+DateSplit+"%m"+DateSplit+"%d"
    aimDate = (datetime.datetime.now() - datetime.timedelta(days = days)).strftime(Datetype)
    return aimDate
def get_data(i, j, c_type, headers, connect):
	url = 'https://api.feixiaohao.com/vol/maxchange/?datatype='+c_type+'&timetype='+str(j)+'&searchtype='+str(i)
	rs = requests.get(url, headers=headers)
	print(rs.status_code)
	if rs.status_code != 200:
		print("数据请求失败\n")
		return
	tree = etree.HTML(rs.text)
	r = tree.xpath('//table//tr')
	for record in r:
		rank = record.xpath("./td[1]/span/text()")
		if not rank:
			continue
		rank = rank[0] if len(rank) else 0
		href = record.xpath("./td[2]/a/@href")
		href = href[0] if len(href) else ''
		icon = record.xpath("./td[2]/a/img/@src")
		icon = icon[0] if len(icon) else ''
		name = record.xpath("./td[2]/a/text()")
		name = name[0] if len(name) else ''
		abbreviation = record.xpath("./td[3]/text()")
		abbreviation = abbreviation[0] if len(abbreviation) else ''
		turnover = record.xpath("./td[4]/a/text()")
		turnover = turnover[0] if len(turnover) else ''
		price = record.xpath("./td[5]/a/text()")
		price = price[0] if len(price) else ''
		percentage = record.xpath("./td[6]/span/text()")
		percentage = percentage[0] if len(percentage) else ''
		data_type = c_type
		search_type = i 
		time_type = j
		rp_date = getTime(0,'-')
		sql = "REPLACE INTO upanddowns (rank,href,icon,name,abbreviation,turnover,price,percentage,data_type,search_type,time_type,rp_date) VALUES (%s,'%s','%s','%s','%s','%s','%s','%s','%s',%s,%s,'%s')"
		data = (rank,href,icon,name,abbreviation,turnover,price,percentage,data_type,search_type,time_type,rp_date)
		connect['cur'].execute(sql % data)
		connect['con'].commit()
		print('成功插入', connect['cur'].rowcount, '条数据')
def connect1():
	connect = pymysql.Connect(
		host='localhost',
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
	main()