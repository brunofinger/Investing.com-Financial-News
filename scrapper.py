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






