import requests
import re
from bs4 import BeautifulSoup
import os
import threading
import mer_urls
import sys
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
    with requests.Session() as session:
        response = session.post(url, headers=headers, data=data, verify=False)
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


def validate_m3u8_url(url, name):
    try:
        # 发送HTTP请求获取M3U8文件内容
        with requests.get(url, timeout=10) as response:
            response.raise_for_status()
            if response.status_code == 200:
                valid_m3u8_link.append(url)
                print(f"{url}\n{name}M3U8链接有效")
                return url

    # except requests as e:
    except requests.exceptions.RequestException as e:
        result = f"{url}\nError: {name} 无效链接. Exception: {e}"
        print(result)
        return result
    except Exception as e:
        # 处理其他异常，例如超时
        result = f"{url}\nError: {name} 其他异常. Exception: {e}"
        print(result)
        return result


# 检测有效链接，并写入m3u8_url.txt
def detectLinks(name, m3u8_list, TV_name):
    thread = []
    for m3u8_url in m3u8_list:
        t = threading.Thread(target=validate_m3u8_url, args=(m3u8_url, name,))
        t.setDaemon(True)  # 设置为守护线程,确保在主线程退出时，所有子线程都会被强制终止
        t.start()
        thread.append(t)
    # 等待所有线程完成
    for t in thread:
        try:
            print(f"Waiting for thread {t} to finish")
            t.join(timeout=5)  # 等待线程超时
        except Exception as e:
            print(f"Thread {t} raised an exception: {e}")
    # 检测的valid_m3u8_link列表，保存到m3u8_url.txt文本中
    time.sleep(10)
    # 判断TV_names列表中的文件夹是否存在
    if not os.path.exists(f'{TV_name}'):
        os.makedirs(f'{TV_name}')
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
    # 遍历当前文件下的txt文件,提取文件名
    TV_names = [os.path.splitext(f)[0] for f in os.listdir(current_directory) if f.endswith(".txt")]
    # TV_names = ['🇭🇰港台']
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
