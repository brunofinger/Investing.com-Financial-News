import os
from bs4 import BeautifulSoup
from multiprocessing import Pool


CPU_COUNT = 4
def open_text_file(file_txt):
	with open(file_txt, "r") as file:
		soup = BeautifulSoup(file, "html.parser")
	soup = soup.find('div', {'class':'largeTitle'})
	return soup.findAll('article')

def create_tasks(path):
	return os.listdir(path)

def extract_id(soup):
	return soup['data-id']

def extract_image(soup):
	soup = soup.find('a')
	return soup.find('img')['data-src']

def extract_title(soup):
	soup = soup.find('div')
	url = soup.find('a')['href']
	title = soup.find('a').text
	return(url, title)

def extract_text(soup):
	soup = soup.find('div')
	return soup.find('p').text

path = '/home/finger/Documents/investing_news/'
finews = {}

def handler(file):
	news = open_text_file(path+file)
	investing_url = 'https://www.investing.com'
	for n in news:
		id = extract_id(n)
		image_url = extract_image(n)
		url, title = extract_title(n)
		text = extract_text(n)

		finews[id] = { 'url' : investing_url+url,
						'image' : image_url,
						'title' : title,
						'text' : text}

	print(finews)


task = create_tasks(path)

with Pool(CPU_COUNT) as pool:
	pool.map(handler, task)
