from concurrent.futures import ThreadPoolExecutor, wait
import requests
import re
from bs4 import BeautifulSoup
import os
# 消除由urllib3库生成的警告，即在不验证SSL证书的情况下访问HTTPS网站
import urllib3
import mer_urls
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        response.raise_for_status()
        if response.status_code == 200:
            valid_m3u8_link.append(url)
            print(f"{url}\nM3U8链接有效")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        # return False


# 检测有效链接，并写入m3u8_url.txt
def detectLinks(name, m3u8_list, TV_name):
    # 多线程测试m3u8的链接有效性
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(validate_m3u8_url, m3u8_url) for m3u8_url in m3u8_list]

        # Wait for all tasks to complete
        # 等待所有任务完成
        wait(futures)
        # for future in futures:
        #     future.result()
    # 检测的valid_m3u8_link列表，保存到m3u8_url.txt文本中
    with open(os.path.join(f'{TV_name}', f'{name}.txt'), 'w', encoding='utf-8') as file:
        for valid_url in valid_m3u8_link:
            file.write(f'{name},{valid_url}\n')
        valid_m3u8_link.clear()


if __name__ == '__main__':
    tv_dict = {}
    valid_m3u8_link = []
    # TV_names = ['🇨🇳央视频道', '卫视频道', '🇭🇰港台']
    TV_names = ['卫视频道', '🇭🇰港台']
    for TV_name in TV_names:
        # 读取文件并逐行处理
        with open(f'{TV_name}.txt', 'r', encoding='utf-8') as file:
            names = [line.strip() for line in file]
            for name in names:
                m3u8_list = get_url(name)
                tv_dict[name] = m3u8_list
                print(name)
            print(tv_dict)
        for name, m3u8_list in tv_dict.items():
            detectLinks(name, m3u8_list, TV_name)
        # 合并m3u8链接
        mer_urls.mer_links(TV_name)
        tv_dict.clear()
