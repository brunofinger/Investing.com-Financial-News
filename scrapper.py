import os
from multiprocessing import Pool
import multiprocessing as mp
import json
from bs4 import BeautifulSoup
import logging
import sys
import time
from pprint import pprint
import csv

log = logging.getLogger(__name__)

LOGGER = {
		'datefmt'  : '%Y-%m-%d %H:%M:%S',
		'format'   : f'[%(asctime)s.%(msecs)03d]'
					 f'[%(process)s]'
				     f'[%(funcName)s:%(lineno)d]'
				     f'[%(levelname)s]'
				     f': %(message)s',
		'level'    : logging.DEBUG,
		'stream'   : sys.stdout
}
CPU_COUNT = (os.cpu_count() // 2) + 1



class Scrapper:

    def __init__(self, path) -> None:
        self.path = path

    def create_tasks(self):
        return os.listdir(self.path)

    def open_text_file(self, file_txt):
        with open(file_txt, "r") as file:
            return BeautifulSoup(file, "html.parser")

    def handler():
        pass

    def extract_info(self, tasks):
        # tasks = self.create_tasks()
        manager = mp.Manager()
        queue = manager.Queue()
        count = len(tasks)
        data = {}

        with Pool(CPU_COUNT) as pool:
            pool.starmap(self.handler, [(t, queue) for t in tasks])
            while count > 0:
                item = queue.get()
                if item is None:
                    count -= 1
                else:
                    id, value = item
                    data[id] = value

        return data #(news, {'total_pages' : len(tasks), 'total_news' : len(news)})

    def download_json(self, file_name, content)-> None:
        print('Creating json ', file_name)
        file_name = file_name if file_name.endswith('.json') else file_name + '.json'
        with open(self.path+file_name, 'w', encoding='utf8') as  file:
            json.dump(content, file, indent=4)

    def download_csv(self, file_name, data):
        file_name = file_name if file_name.endswith('.csv') else file_name + '.csv'
        values = []
        for k, v in data.items():
            d = {'id_news': k}
            d.update(v)
            values.append(d)

        with open(self.path+file_name, 'w') as csvfile:
            fields = values[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames = fields)
            writer.writeheader()
            writer.writerows(values)

    # def download_csv(self,)

class ScrapperInvesting(Scrapper):

    def __init__(self, path) -> None:
        self.path = path if path.endswith('/') else path + '/'
        # self.investing = ScrapperInvesting
        self.base_url = 'https://www.investing.com'

    def extract_id(self, soup):
        # print(soup)
        return soup['data-id']

    def extract_image(self, soup):
        soup = soup.find('a')
        return soup.find('img')['data-src']

    def extract_title(self, soup):
        soup = soup.find('div')
        url = soup.find('a')['href']
        title = soup.find('a').text
        return(url, title)

    def extract_text(self, soup):
        soup = soup.find('div')
        text = soup.find('p').text
        return text.replace('\n', '')

    def handler(self, file, queue):
        try:
            soup = self.open_text_file(self.path+file)
            soup = soup.find('div', {'class':'largeTitle'})
            articles = soup.findAll('article')
            for n in articles:
                try:
                    id = self.extract_id(n)
                    image_url = self.extract_image(n)
                    url, title = self.extract_title(n)
                    id = url.split('-')[-1]
                    text = self.extract_text(n)

                    values = { 'url' : self.base_url+url,
                            'tag' : 'economy',
                            'image' : image_url,
                            'title' : title,
                            'text' : text}
                    print(f"URL: {values['url']}, FILE: {file}")
                    queue.put([id, values])
                except KeyError:
                    pass
        except AttributeError:
            pass
        queue.put(None)




# def main() -> None:
#     logging.basicConfig(**LOGGER)

#     path = '/home/finger/Documents/Investing.com-Financial-News/news_economy_'

#     scrapper = ScrapperInvesting(path)
#     tasks = scrapper.create_tasks()
#     news = scrapper.extract_info(tasks)

#     scrapper.download_json(file_name= f'economy_news.json', content=news)
#     scrapper.download_csv(file_name= f'economy_news', data=news)

#     print('Scrapping completed')
# if __name__ == "__main__":
#     main()

# # EOF#






