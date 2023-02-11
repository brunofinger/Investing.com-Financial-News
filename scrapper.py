import os
from multiprocessing import Pool
import multiprocessing as mp
import json
from bs4 import BeautifulSoup
import logging
import sys
import time
from pprint import pprint

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

class ScrapperInvesting:

    def extract_id(soup):
        # print(soup)
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
        text = soup.find('p').text
        return text.replace('\n', '')

class Scrapper:

    def __init__(self, path) -> None:
        self.path = path
        self.investing = ScrapperInvesting
        self.base_url = 'https://www.investing.com'
        self.news = {}

    def create_tasks(self):
        return os.listdir(self.path)

    def open_text_file(self, file_txt):
        with open(file_txt, "r") as file:
            soup = BeautifulSoup(file, "html.parser")
        soup = soup.find('div', {'class':'largeTitle'})
        return soup.findAll('article')


    def handler(self, file, queue):
        articles = self.open_text_file(self.path+file)
        topic = ['cryptocurrency', 'bitcoin']
        for n in articles:
            try:
                id = self.investing.extract_id(n)
                image_url = self.investing.extract_image(n)
                url, title = self.investing.extract_title(n)
                id = url.split('-')[-1]
                text = self.investing.extract_text(n)

                values = { 'url' : self.base_url+url,
                        'tag' : [item for item in topic if item in url.split('/')],
                        'image' : image_url,
                        'title' : title,
                        'text' : text}
                log.info(f"{values['url']}")
                queue.put([id, values])
            except KeyError:
                pass
        queue.put(None)

    def extract_info(self):
        tasks = self.create_tasks()
        manager = mp.Manager()
        queue = manager.Queue()
        count = len(tasks)
        news = {}

        with Pool(CPU_COUNT) as pool:
            pool.starmap(self.handler, [(t, queue) for t in tasks])
            while count > 0:
                item = queue.get()
                if item is None:
                    count -= 1
                else:
                    id, value = item
                    news[id] = value

        return (news, {'total_pages' : len(tasks), 'total_news' : len(news)})

def download_json(file_name, content)-> None:
    with open(file_name, 'w', encoding='utf8') as  file:
        json.dump(content, file, indent=4)


def main() -> None:
    logging.basicConfig(**LOGGER)

    path = ''

    t0 = time.time()

    news, stats = Scrapper(path=path).extract_info()
    download_json(file_name='news.json', content=news)

    total_time = round(time.time() - t0, 2)
    stats['total_time'] = f"{round(total_time/60, 2)} min" if total_time >= 60 else f"{round(total_time, 2)} s"
    stats['average_time_per_page'] = round(total_time/stats['total_pages'], 5) + ' s'
    stats['average_time_per_news'] = round(total_time/stats['total_news'], 5) + ' s'

    download_json(file_name='stats_news.json', content=stats)

    pprint(stats)

if __name__ == "__main__":
    main()

# EOF#






