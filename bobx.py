#!/usr/bin/python

import os
import sys
import urllib2
import re
from bs4 import BeautifulSoup
import requests
import threading

domain = 'http://www.bobx.com'
count = 0
def get_url(url):
	print 'Opening', url
	global count
	count = count + 1
	print count
	headers = {'User-Agent': 'Mozilla/5.0'}
	f = requests.get(url,headers=headers).text
	soup = BeautifulSoup(f)
	href_lists = []
	for link in soup.find_all('a'):
		href_lists.append(link.get('href'))
	print href_lists
	return list(set(href_lists))

def get_img_url(url):
	print 'Opening', url
	headers = {'User-Agent': 'Mozilla/5.0'}
	f = requests.get(url,headers=headers).text
	soup = BeautifulSoup(f)
	href_lists = []
	for link in soup.find_all('img'):
		href_lists.append(link.get('src'))
	return list(set(href_lists))

def get_series(index_page):
	href_lists = get_url(index_page)
	print href_lists
	series_lists = []
	for i in href_lists:
		if re.search('.+series.+html', str(i)):
			series_lists.append(i)
	series_lists = list(set(series_lists))
	
	series_lists = [domain+link for link in series_lists]

	return series_lists


def get_large_pic_url(series_lists):
	result_lists = []
	for i in series_lists:
		t = threading.Thread(target=get_url,kwargs={'url':i})
		t.start()
##		href_lists = get_url(i)
##		large_lists = []
##		for i in href_lists:
##			if re.search('.+large.+/', i):
##				large_lists.append(i)
##		large_lists = [domain+link for link in large_lists]
##
##		result_lists = result_lists + large_lists
##
##	return result_lists
	

def get_jpg(large_url_lists):
	jpg_lists = []
	for i in large_url_lists:
		jpg_url_lists = get_img_url(i)
		jpg_url = domain + jpg_url_lists[0]
		jpg_lists.append(jpg_url)
		
	return list(set(jpg_lists))
		

def return_html(jpg_lists):
	first_html = '''
	<html>
		<head>
			<title>hello</title>
		</head>
		<body>'''
	jpg_html = ''
	for i in jpg_lists:
		jpg_html = jpg_html + '<img src="' + i + '" width=auto height=100%>' + '<br>' + '\n'
	second_html = '''
		</body>
	</html>'''	

	return first_html+jpg_html+second_html

def return_txt(jpg_lists):
	txt = ''
	for i in jpg_lists:
		txt = txt + i + "\n"
	return txt

def main():
	reload(sys)
	sys.setdefaultencoding('utf-8')
	series_lists = get_series(sys.argv[1])
	get_large_pic_url(series_lists)
	print "done"

if __name__ == '__main__':
	main()
