from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor



def create_text_file(name, content, path):
	with open(f"{path}{name}.txt", "w") as file:
		file.write(content)

def pageSource(url):
	headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:108.0) Gecko/20100101 Firefox/108.0'}
	req = Request(url,headers=headers)
	res = urlopen(req)
	print(url, res.getcode())
	return str(BeautifulSoup(res, 'html.parser'))

def create_tasks(urls):
    return [url.format(i) for url, n in urls.items() for i in range(1, n+1)]

def handler(url):
	create_text_file(content= pageSource(url),
                    name = '_'.join(url.split('/')[3:]),
                    path = '/home/finger/Documents/investing_news/')

def main():
    urls = {'https://www.investing.com/news/cryptocurrency-news/{}' : 2,
            'https://www.investing.com/crypto/bitcoin/news/{}' : 2}

    with ThreadPoolExecutor(max_workers=20) as executor:
        tasks = create_tasks(urls)
        results = executor.map(handler, tasks)

if __name__ == "__main__":
	main()

# EOF#
