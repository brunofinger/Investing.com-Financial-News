
# 📰 Investing.com Financial News Scraper

This Python script scrapes the latest financial news articles from Investing.com and stores them in a CSV file.

## 🚀 How It Works

The script first fetches the HTML of Investing.com's news page and parses it using Beautiful Soup. It then loops through each article on the page and extracts the title, date, author, and content of the article. 

The script cleans the data by removing any unwanted characters and formats it into a CSV file. By default, the script saves the data to a file called `investing_news.csv`. 

You can customize the script to scrape news from different categories or regions by changing the URL in the `BASE_URL` variable. You can also modify the script to scrape additional information from the articles or to save the data in a different format. 

## 📝 How To Use

1.  Install the `beautifulsoup4` and `requests` packages by running `pip install beautifulsoup4 requests`.
2.  Clone this repository or download the `investing_news_scraper.py` file.
3.  Navigate to the directory containing the `investing_news_scraper.py` file.
4.  Open a terminal or command prompt and run the script using the command `python investing_news_scraper.py`.
5.  The script will scrape the latest news articles and save them to a CSV file called `investing_news.csv`.
6.  Optionally, you can modify the script to scrape news from different categories or regions by changing the URL in the `BASE_URL` variable.
7.  You can also modify the script to scrape additional information from the articles or to save the data in a different format.

## 📥 Download the Financial News Big Data from Investing dataset from Kaggle [here](https://www.kaggle.com/datasets/fingerbruno/financial-news-big-data-from-investing-website) and start analyzing financial news data today!
