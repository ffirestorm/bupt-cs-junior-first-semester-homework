from urllib.parse import urlsplit
import requests
from bs4 import BeautifulSoup
import re
import os

urls = open('./data/urls/urls.txt').read().split('\n')
count = 36240

urls = urls[count:]

for url in urls:
    if not url.startswith("http://www.chinanews.com/"):
        continue
    parsed_url = urlsplit(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    path_parts = parsed_url.path.split('/')
    year = path_parts[2] 
    if not year.isdigit() :
        continue
    type = path_parts[1]
    count += 1
    
    # 开始获取文本信息
    try:
        response = requests.get(url, timeout=5)
    except requests.Timeout:
        print("{} timeout".format(count))
        continue
    except requests.exceptions.RequestException as e:
        print(f"请求发生错误: {e}")
    response.encoding = 'gb2312' if int(year) < 2019  else 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找 left_zw 类（用来保存新闻内容的）
    left_zw = soup.find('div', class_='left_zw')
    if left_zw:
        # 提取文本内容
        news_contents = ''
        paragraphs = left_zw.find_all('p')
        for paragraph in paragraphs:
            news_contents += paragraph.text.strip()
        
        # 创建保存路径
        filepath = f'./data/news/{type}/'
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        # 保存到文件
        filename = f'{filepath}{str(count)}.txt'
        with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
            f.write(news_contents)
        print(count)