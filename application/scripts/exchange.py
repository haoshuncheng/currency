import requests
from lxml import etree
import pymysql.cursors
import sys
import json

def main():
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	connect = connect1()
	for i in range(1, 100):
		print("获取："+str(i)+"页数据")
		get_data(i, headers, connect)
	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()
def getTime(days = 1,DateSplit=None):
    if not DateSplit:
        Datetype = "%Y%m%d"
    else:
        Datetype = "%Y"+DateSplit+"%m"+DateSplit+"%d"
    aimDate = (datetime.datetime.now() - datetime.timedelta(days = days)).strftime(Datetype)
    return aimDate
def get_data(i, headers, connect):
	rs = requests.get('https://www.feixiaohao.com/exchange/list_'+str(i)+'.html?mineable=1', headers=headers)
	#rs = requests.get('https://www.feixiaohao.com/list_1.html', headers=headers)
	print(rs.status_code)
	if rs.status_code != 200:
		print("数据请求失败\n")
		return
	tree = etree.HTML(rs.text)
	r = tree.xpath('//tbody/tr')
	for record in r:
		rank = record.xpath("./td[1]/text()")
		rank = rank[0] if len(rank) else 0

		href = record.xpath("./td[2]/a/@href")
		href = href[0] if len(href) else ''

		icon = record.xpath("./td[2]/a/img/@src")
		icon = icon[0] if len(icon) else ''

		name = record.xpath("./td[2]/a/text()")
		name = name[0] if len(name) else ''

		turnover = record.xpath("./td[3]/a/text()")
		turnover = turnover[0] if len(turnover) else ''

		transaction_pair = record.xpath("./td[4]/a/text()")
		transaction_pair = transaction_pair[0] if len(transaction_pair) else 0

		country = record.xpath("./td[5]/a/text()")
		country = country[0] if len(transaction_pair) else ''

		transaction_types = record.xpath("./td[5]")

		print(transaction_types)
		

		stars = record.xpath("./td[6]/div/@class")
		stars = stars[0] if len(stars) else ''

		follows = record.xpath("./td[6]/div/text()")
		follows = follows[0] if len(follows) else 0 

		rp_date = getTime(0,'-')

		sql = "REPLACE INTO exchange (rank,href,icon,name,turnover,transaction_pair,country,transaction_types,stars,follows,rp_date) VALUES (%s,'%s','%s','%s','%s',%s,'%s','%s','%s',%s,'%s')"
		print(sql)
		data = (rank,href,icon,name,turnover,transaction_pair,country,transaction_types,stars,follows,rp_date)
		print(data)
		connect['cur'].execute(sql % data)
		connect['con'].commit()
		print('成功插入', connect['cur'].rowcount, '条数据')
		#print(alt)
	#print(len(r))

	# r = tree.xpath('//tr[@id="bitcoin"]/td[@class="change"]/span/@class')
	# print(r)

	# f = open('./abc.html', 'w', encoding='utf-8')
	# f.write(rs.text)
	# f.close()

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