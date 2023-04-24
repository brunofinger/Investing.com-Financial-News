from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import os
import urllib.request

class Crawler:

    def __init__(self, url, max_workers, directory_path, total_pages) -> None:
        self.url = url.strip("/")
        self.max_workers = max_workers
        self.directory_path = directory_path.rstrip("/") + "/"
        self.total_pages = total_pages

    def create_directory(self, overwrite=False, directory_name=None):
        directory_name = directory_name or self.url.split("/")[-1]
        directory_path = os.path.join(self.directory_path, directory_name)
        if os.path.exists(directory_path):
            if overwrite:
                self.directory_path = directory_path
                return directory_path
            else:
                raise ValueError("Directory already exists and overwrite is False")
        os.makedirs(directory_path)
        self.directory_path = directory_path
        return directory_path

    def get_page_source(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'}
        req = urllib.request.Request(url, headers=headers)
        res = urllib.request.urlopen(req)
        print(url, res.getcode())
        return str(BeautifulSoup(res, "html.parser"))

    def create_tasks(self):
        url_template = f"{self.url}/{{}}" if self.url.endswith("/") else f"{self.url}/{{}}"
        return [url_template.format(n) for n in range(1, self.total_pages + 1)]

    def save_page_source(self, url):
        file_name = url.split("/")[-1] + ".txt"
        file_path = os.path.join(self.directory_path, file_name)
        with open(file_path, "w") as file:
            file.write(self.get_page_source(url))

    def run(self):
        tasks = self.create_tasks()
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(self.save_page_source, tasks)
