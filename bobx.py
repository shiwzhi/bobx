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
result_list = []
img_list = []
thread_list = []
jpg_list = []
thread_list_jpg = []
def get_url(url):
	print 'Opening', url
	headers = {'User-Agent': 'Mozilla/5.0'}
	f = requests.get(url,headers=headers).text
	soup = BeautifulSoup(f)
	href_lists = []
	for link in soup.find_all('a'):
		href_lists.append(link.get('href'))
	global count
	count = count + 1
	print count
	global result_list
	result_list.append(set(href_lists))
	return list(set(href_lists))

def get_ser_url(url):
        print 'Opening', url
        headers = {'User-Agent': 'Mozilla/5.0'}
        f = requests.get(url,headers=headers).text
        soup = BeautifulSoup(f)
        href_lists = []
        for link in soup.find_all('a'):
                href_lists.append(link.get('href'))
        return list(set(href_lists))

def get_img_url(url):
	headers = {'User-Agent': 'Mozilla/5.0'}
	f = requests.get(url,headers=headers).text
	print "success opened " + url
	soup = BeautifulSoup(f)
	href_lists = []
	for link in soup.find_all('img'):
		href_lists.append(link.get('src'))
	global jpg_list
	jpg_list.append(list(set(href_lists))[0])
	return list(set(href_lists))

def get_series(index_page):
	href_lists = get_ser_url(index_page)
	series_lists = []
	for i in href_lists:
		if re.search('.+series.+html', str(i)):
			series_lists.append(i)
	series_lists = list(set(series_lists))
	
	series_lists = [domain+link for link in series_lists]
	print series_lists
	return series_lists


def get_large_pic_url(series_lists):
	for i in series_lists:
		t = threading.Thread(target=get_url,kwargs={'url':i})
		global thread_list
		thread_list.append(t)
		t.start()
##		href_lists = get_url(i)

	large_lists = []
	for i in thread_list:
		i.join()

	for i in result_list:
		for j in i:
			if re.search('.+large.+/',str(j)):
				large_lists.append(j)
	return [domain+link for link in large_lists]
'''
		if re.search('.+large.+/', i):
			large_lists.append(i)
		large_lists = [domain+link for link in large_lists]
	print large_lists
'''
###
##		result_lists = result_lists + large_lists
##
##	return result_lists


def get_jpg(large_url_lists):
	jpg_lists = []
	for i in large_url_lists:
		t = threading.Thread(target=get_img_url,kwargs={'url':i})
		global thread_list_jpg
		thread_list_jpg.append(t)
		t.start()
	for i in thread_list_jpg:
		i.join()
	return [domain+link for link in jpg_list]

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
	large_lists = get_large_pic_url(series_lists)
	jpg = get_jpg(large_lists)
	jpg = list(set(jpg))
	if sys.argv[2] == '-w':
		f = open(sys.argv[3],'w')
		for i in jpg:
			print "Writing "+i
			f.write(i+'\n')
		f.close()
		print "Writed to "+sys.argv[3]
if __name__ == '__main__':
	main()
