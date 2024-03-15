
from urllib.parse import urlsplit
import requests
from bs4 import BeautifulSoup
import os
import threading

type_list = ["fz", "business", "edu", "mil", "ny", "house"]

def fetch_and_save(urls, count):
    try:
        for url in urls:
            if not url.startswith("http://www.chinanews.com/"):
                continue
            parsed_url = urlsplit(url)
            # base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            path_parts = parsed_url.path.split('/')
            year = path_parts[2] 
            if not year.isdigit() :
                continue
            type = path_parts[1]
            count += 1
            if type not in type_list:
                continue
            filepath = f'./data/news/{type}/'
            if not os.path.exists(filepath):
                os.makedirs(filepath)
            filename = f'{filepath}{str(count)}.txt'
            if os.path.exists(filename):
                continue

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
                
                # 保存到文件
                with open(filename, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(news_contents)
                print("完成：{} 的读取".format(count))
    except  Exception as e:
        print(f"{count} 发生错误: {e}")



if __name__ == "__main__":
    urls = open('./data/urls/urls.txt').read().split('\n')
    base_count = 36240

    urls = urls[base_count:]
    chunk_size = 10000
    finished_num = 5000
    threads = []
    try:
        for i in range(base_count, len(urls), chunk_size):
            base = i + finished_num
            thread = threading.Thread(target=fetch_and_save, args=(urls[base:i+chunk_size], base))
            threads.append(thread)
            thread.start()
            print("开启线程: {}".format(i))
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
    except Exception as e:
        print("出现问题:{}".format(e))