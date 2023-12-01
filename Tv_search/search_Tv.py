from concurrent.futures import ThreadPoolExecutor, wait
import requests
import re
from bs4 import BeautifulSoup
import os
import threading
# 消除由urllib3库生成的警告，即在不验证SSL证书的情况下访问HTTPS网站
import urllib3
import mer_urls
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time


def get_url(name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    url = "http://tonkiang.us/"
    # 获取两页的m3u8链接
    # params = {
    #     "page": 1,
    #     "s": name
    # }
    # response = requests.get(url, headers=headers, params=params, verify=False)
    data = {
        "search": name,
        "Submit": " "
    }
    response = requests.post(url, headers=headers, data=data, verify=False)
    response.close()
    print(response)
    # print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the div with class "m3u8"
    m3u8_divs = soup.find_all('div', class_='m3u8')
    m3u8_list = []
    for div in m3u8_divs:
        # Extract the HTTP link from the onclick attribute
        onclick_value = div.find('img')['onclick']
        url_match = re.search(r'copyto\("([^"]+)"\)', onclick_value)

        if url_match:
            extracted_url = url_match.group(1)
            print(extracted_url)
            m3u8_list.append(extracted_url)
        # else:
        #     print("URL extraction failed.")
    return m3u8_list


def validate_m3u8_url(url):
    try:
        # 发送HTTP请求获取M3U8文件内容
        response = requests.get(url, timeout=2)
        response.close()
        response.raise_for_status()
        if response.status_code == 200:
            valid_m3u8_link.append(url)
            print(f"{url}\nM3U8链接有效")

    # except requests as e:
    except requests.exceptions.RequestException as e:
        print(f"{url}\nError无效链接")
        # return False


# 检测有效链接，并写入m3u8_url.txt
def detectLinks(name, m3u8_list, TV_name):
    # 多线程测试m3u8的链接有效性
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     futures = [executor.submit(validate_m3u8_url, m3u8_url) for m3u8_url in m3u8_list]
    #     # 等待所有任务完成
    #     wait(futures)
    # 单线程测试m3u8的链接有效性
    thread = []
    for m3u8_url in m3u8_list:
        t = threading.Thread(target=validate_m3u8_url, args=(m3u8_url,))
        t.start()
        thread.append(t)
    # 等待所有线程完成
    for t in thread:
        print(f"Waiting for thread {t} to finish")
        t.join()
        # validate_m3u8_url(m3u8_url)
    # 检测的valid_m3u8_link列表，保存到m3u8_url.txt文本中
    time.sleep(10)
    with open(os.path.join(f'{TV_name}', f'{name}.txt'), 'w', encoding='utf-8') as file:
        for valid_url in valid_m3u8_link:
            file.write(f'{name},{valid_url}\n')
        valid_m3u8_link.clear()
        sys.stdout.flush()


if __name__ == '__main__':
    # 获取当前工作目录
    current_directory = os.getcwd()
    # 构造上级目录的路径
    parent_dir = os.path.dirname(current_directory)
    output_file_path = os.path.join(parent_dir, 'live.txt')
    # 清空live.txt内容
    with open(output_file_path, 'w', encoding='utf-8') as f:
        pass
    tv_dict = {}
    valid_m3u8_link = []
    TV_names = ['🇨🇳央视频道', '卫视频道', '🇭🇰港台']
    # TV_names = ['卫视频道', '🇭🇰港台']
    for TV_name in TV_names:
        # 读取文件并逐行处理
        with open(f'{TV_name}.txt', 'r', encoding='utf-8') as file:
            names = [line.strip() for line in file]
            for name in names:
                m3u8_list = get_url(name)
                tv_dict[name] = m3u8_list
                print(name)
            print('---------字典加载完成！------------')
        for name, m3u8_list in tv_dict.items():
            detectLinks(name, m3u8_list, TV_name)
        # 合并m3u8链接
        mer_urls.mer_links(TV_name)
        tv_dict.clear()
