from bs4 import BeautifulSoup
import requests
from multiprocessing import Pool

bobx = 'http://www.bobx.com'

def get_soup(link):
	print("Opening "+link)
	r = requests.get(link)
	soup = BeautifulSoup(r.text, 'lxml')
	return soup


def from_home_get_series(home_link):
	soup = get_soup(home_link)
	link = soup.find_all('a', 'smallblack', "_top")
	link1 = []
	for i in link:
		if "offset" in i['title']:
			link1.append(bobx+i['href'])
	return link1

def from_serie_get_large(serie_link):
	soup = get_soup(serie_link)
	link = []
	for i in soup.find_all('td', align = 'right'):
		if i.contents[0].name == 'a':
			link.append(bobx+i.contents[0]['href'])
	return link

def from_large_get_large_jpg(large_link):
	soup = get_soup(large_link)
	link = soup.find('img', border='0')
	return bobx+link['src']


def from_home_get_large_jpg(home_link):
	series = from_home_get_series(home_link)
	p = Pool(300)
	large_list = p.map(from_serie_get_large, series)
	jpg_list = []

	for i in large_list:
		jpg_list += p.map(from_large_get_large_jpg, i)
	return jpg_list