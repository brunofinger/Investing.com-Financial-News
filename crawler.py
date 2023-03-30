from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor
from os import path, makedirs


class Crawler:

    def __init__(self, url,  max_workers, path, total_pages) -> None:
        self.url = url if path.endswith('/') else url + '/'
        self.max_workers = max_workers
        self.path = path if path.endswith('/') else path + '/'
        self.total_pages = total_pages

    def create_folder(self, overwrite = False, folder_name = None):
        if not folder_name:
            folder_name = self.url.replace('/', '_').split('com')[-1][1:] + '/'

        folder_name =self.path + folder_name + '/'
        print(folder_name)
        if not path.exists(folder_name):
            makedirs(folder_name)
            self.path = folder_name
            return folder_name
        elif overwrite:
            self.path = folder_name
            return folder_name
        else:
            raise AttributeError('Folder  already exits in this path')

    def pageSource(self, url):
        headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'}
        req = Request(url,headers=headers)
        res = urlopen(req)
        print(url, res.getcode())
        return str(BeautifulSoup(res, 'html.parser'))

    def create_tasks(self):
        url = self.url + '{}' if self.url.endswith('/') else self.url + '/{}'
        return [url.format(n) for n in range(1, self.total_pages)]

    def handler(self, url):
        file_name = url.replace('/', '_').split('.com')[-1][1:]
        with open(f"{self.path}{file_name}.txt", "w") as file:
            file.write(self.pageSource(url))

    def run(self):
        tasks = self.create_tasks()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.handler, tasks)


