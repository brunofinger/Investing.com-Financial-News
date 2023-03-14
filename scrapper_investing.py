import os
# from multiprocessing import Pool
# import multiprocessing as mp
# import json
# from bs4 import BeautifulSoup
import logging
import sys
from scrapper import Scrapper
from crawler import Crawler


log = logging.getLogger(__name__)

LOGGER = {
		'datefmt'  : '%Y-%m-%d %H:%M:%S',
		'format'   : f'[%(asctime)s.%(msecs)03d]'
					 f'[%(process)s]'
				     f'[%(funcName)s:%(lineno)d]'
				     f'[%(levelname)s]'
				     f': %(message)s',
		'level'    : logging.INFO,
		'stream'   : sys.stdout
}
CPU_COUNT = (os.cpu_count() // 2) + 1



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
                            'tag' : 'commodities',
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




def main() -> None:
    logging.basicConfig(**LOGGER)

    crawler = Crawler(
        max_workers = 100,
        path = '/home/finger/Documents/Investing.com-Financial-News',
        url = 'https://www.investing.com/news/commodities-news',
        total_pages = 2475
    )

    path = crawler.create_folder(overwrite=True, folder_name='commodities_news')
    crawler.run()
    scrapper = ScrapperInvesting(path)
    tasks = scrapper.create_tasks()
    news = scrapper.extract_info(tasks)

    scrapper.download_json(file_name= f'commodities_news', content=news)
    scrapper.download_csv(file_name= f'commodities_news', data=news)

    print('Scrapping completed')
if __name__ == "__main__":
    main()

# EOF#






