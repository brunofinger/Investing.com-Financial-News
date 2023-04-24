
## 📰  Investing.com Financial News Scraper

This repository contains a web scraper for financial news from Investing.com, which uses multithreading to download the pages and multiprocessing to extract data from the pages. The scraped data is then stored in a SQL table using bulk insert.

### 🚀 How to use

1.  Clone the repository to your local machine.
2.  Install the required packages listed in the `requirements.txt` file.
3.  Set up a SQL database and modify the `config.py` file to include your database credentials.
4.  Run `crawler.py` to download the web pages and `scrapper.py` to extract the data and store it in the SQL database.

### 📥 Download the data

The scraped data can be downloaded from the following Kaggle dataset: [https://www.kaggle.com/datasets/fingerbruno/financial-news-big-data-from-investing-website](https://www.kaggle.com/datasets/fingerbruno/financial-news-big-data-from-investing-website)

The dataset contains two tables:

-   `news`: contains information about each news article, including the title, date, and URL.
-   `articles`: contains the full text of each news article.
