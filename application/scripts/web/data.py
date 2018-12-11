#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
from lxml import etree
#import pymysql.cursors
import sys
import time
import os
import json

def main():
	tree = get_requests(FIRST_URL)
	get_inf(tree) #获取教师列表

	r = tree.xpath('//ul[@class="'+PAGE_CLASS+'"]/li/a/@href')   #页码
	for url in r:
		print("获取下一页数据："+HOST_URL+url+"\n")
		tree = get_requests(HOST_URL+url)
		get_inf(tree) #获取教师列表


#获取教师列表进入详细页
#cus_Institution:院校名称,cus_Department:系名,name:名称,title:头衔 职称,pic:头像,company:单位学校,email:邮箱,seniority:资历,subject_areas:学科领域,college:学院,faculty_association:教师协会,people_type:人物类型
def get_inf(tree):
	r = tree.xpath('//div[@id="listing_441106"]//a/@href')   #详细页面地址
	if len(r) == 0:
		print("该页教师列表为空")
		return
	for i in r:
		tree_inf = get_requests(HOST_URL+i)
		if tree_inf == False:
			print(i+"：详情页获取失败\n")
			continue
		name = tree_inf.xpath('//h1[@class="page-header row "]/text()')   
		if len(name)==0 or name[0]=='':
			continue
		rec = {"cus_Institution":'Oxford',"cus_Department":'Faculty of Classics'}
		rec['name'] = trim(name[0])                                 											#名称
		get_data(tree_inf, {'title':'//div[@class="field field-name-field-job-title field-type-text field-label-hidden"]//div[@class="field-item private-show even"]/text()','pic':'//div[@class="field field-name-field-teaser-image field-type-image field-label-hidden"]//img/@src','company':'//div[@class="field field-name-field-affiliation field-type-text field-label-hidden"]//div[@class="field-item private-show even"]/text()','email':'//div[@class="field field-name-field-email-address field-type-email field-label-hidden"]//div[@class="field-item private-show even"]/a/text()','seniority':'//div[@class="field field-name-field-further-contact-details field-type-text-with-summary field-label-hidden"]//div[@class="field-item private-show even"]/p[1]/text()','subject_areas':'//div[@class="panel-pane pane-taxonomy-term"]/div[@class="pane-content"]/div/div[1]//a/text()','college':'//div[@class="panel-pane pane-taxonomy-term"]/div[@class="pane-content"]/div/div[2]//a/text()','faculty_association':'//div[@class="panel-pane pane-taxonomy-term"]/div[@class="pane-content"]/div/div[3]//a/text()','people_type':'//div[@class="panel-pane pane-taxonomy-term"]/div[@class="pane-content"]/div/div[4]//a/text()'}, rec)
		save(rec)



#匹配数据
#response文本
#rs规则
def get_data(response, rs, rec):
	for key in rs:
		r = response.xpath(rs[key])
		rec[key] = '' if len(r)==0 else trim(r[0]).replace('\xa0',' ')

def save(rec):
	print(rec)
	with open(os.path.dirname(os.path.abspath(__file__))+"/data/data.txt","a") as f:
		f.write(json.dumps(rec)+"\n")


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