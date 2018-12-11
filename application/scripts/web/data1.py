#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import etree
#import pymysql.cursors
import sys
import time
import os
import json
import csv
import codecs

def main():
	tree = get_requests(FIRST_URL)
	get_inf(tree, FIRST_URL) #获取教师列表

	r = tree.xpath('//ul[@class="'+PAGE_CLASS+'"]/li/a/@href')   #页码
	for url in r:
		print("获取下一页数据："+HOST_URL+url+"\n")
		tree = get_requests(HOST_URL+url)
		get_inf(tree, HOST_URL+url) #获取教师列表


#获取教师列表进入详细页
#cus_Institution:院校名称,cus_Department:系名,name:名称,title:头衔 职称,pic:头像,company:单位学校,email:邮箱,seniority:资历,subject_areas:学科领域,college:学院,faculty_association:教师协会,people_type:人物类型
def get_inf(tree, url):
	r = tree.xpath('//div[@id="listing_441106"]//a')   #详细页面地址
	if len(r) == 0:
		print("该页教师列表为空")
		return
	for i in r:
		href = i.xpath('./@href')   #详细页面地址
		name = i.xpath('.//div[@class="text-box-wrapper generic-text-box"]//div[@class="listing-title"]/h3/text()')   #详细页面地址
		if len(href)==0 or len(name)==0:
			print("详细页面地址或者名称为空\n")
			continue
		rec = ['Oxford Faculty of Classics',url]
		rec.append(name[0])
		tree_inf = get_requests(HOST_URL+href[0])
		if tree_inf == False:
			print(href[0]+"：详情页获取失败\n")
			continue
		res = tree_inf.xpath('string(//div[@class="bootstrap-twocol-stacked"])')
		rec.append(trim_arr(res))
		save(rec)

def trim_arr(res):
	res = res.split("\n")
	if len(res) == 0:
		return ''
	rs1 = []
	for rs in res:
		rs = trim(rs)
		if rs=='':
			continue
		rs1.append(rs)
	return '|||'.join(rs1)

#匹配数据
#response文本
#rs规则
def get_data(response, rs, rec):
	for key in rs:
		r = response.xpath(rs[key])
		rec[key] = '' if len(r)==0 else trim(r[0]).replace('\xa0',' ')

def save(rec):
	print(rec)
	csvfile = codecs.open(os.path.dirname(os.path.abspath(__file__))+'/data/data.csv', 'a', 'utf_8_sig')  #w a r 与文件类似
	writer = csv.writer(csvfile) #文件对象
	writer.writerow(rec) #核心方法
	csvfile.close() #关闭


#发送请求
def get_requests(url):
	headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
	rs = requests.get(url, headers=headers)
	if rs.status_code != 200:
		print("数据请求失败\n")
		return False
	return etree.HTML(rs.text)

#去除字符串两端空格 换行符 回车等
def trim(str):
	return str.strip()

if __name__ == "__main__":
	PAGE_CLASS = 'pagination text-center'
	HOST_URL = 'https://www.classics.ox.ac.uk'
	FIRST_URL = 'https://www.classics.ox.ac.uk/faculty-members'
	main()