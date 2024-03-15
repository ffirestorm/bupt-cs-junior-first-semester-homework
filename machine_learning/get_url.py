# 这个程序是用来爬取 类似 https://www.chinanews.com/scroll-news/2019/1211/news.shtml 这个网站里的url的

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def crawl_news_urls(base_url, year, month, day):
    url = f"{base_url}/{year}/{month:02d}{day:02d}/news.shtml"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    news_urls = []
    for li in soup.select('.content_list ul li'):
        div_bt = li.find('div', class_='dd_bt')
        if div_bt:
            link = div_bt.a
            if link:
                news_url = urljoin(url, link['href'])
                news_urls.append(news_url)

    return news_urls

# 主程序
base_url = "http://www.chinanews.com/scroll-news"

years = [2011,2012, 2013, 2014, 2015, 2016, 2017,2018,2019,2020,2021,2022, 2023]
months = [1, 2, 3,4,5,6,7,8,9,10,11,12]
days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]

# 爬取新闻页面的 URL
with open('./urls.txt', 'a', encoding='utf8') as file:
    for year in years:
        for month in months:
            for day in days:
                news_urls = crawl_news_urls(base_url, year, month, day)
                print(news_urls)
                for news_url in news_urls:
                    file.write(news_url + '\n')
