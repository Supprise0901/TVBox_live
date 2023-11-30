from concurrent.futures import ThreadPoolExecutor
import requests
import re
from bs4 import BeautifulSoup
import os


def validate_m3u8_url(url):
    try:
        # 发送HTTP请求获取M3U8文件内容
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        if response.status_code == 200:
            # 有效链接增加到valid_m3u8_link列表
            valid_m3u8_link.append(url)
            print(f"{url}\nM3U8链接有效")

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return False


# 检测有效链接，并写入m3u8_url.txt
def detectLinks(m3u8_list, name):
    # 多线程测试m3u8的链接有效性
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(validate_m3u8_url, m3u8_url) for m3u8_url in m3u8_list]

        # Wait for all tasks to complete
        for future in futures:
            future.result()

    # 检测的valid_m3u8_link列表，保存到m3u8_url.txt文本中
    with open(os.path.join('tv', f'{name}.txt'), 'w', encoding='utf-8') as file:
        for valid_url in valid_m3u8_link:
            file.write(f'{name},{valid_url}\n')


if __name__ == '__main__':

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    url = "http://tonkiang.us/"
    # 获取两页的m3u8链接
    m3u8_list = []
    for i in range(1, 2):
        print(i)
        params = {
            'page': i,
            "s": "浙江卫视"
        }
        response = requests.get(url, headers=headers, params=params, verify=False)
        print(response)
        # print(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find the div with class "m3u8"
        m3u8_divs = soup.find_all('div', class_='m3u8')

        for div in m3u8_divs:
            # Extract the HTTP link from the onclick attribute
            onclick_value = div.find('img')['onclick']
            url_match = re.search(r'copyto\("([^"]+)"\)', onclick_value)

            if url_match:
                extracted_url = url_match.group(1)
                # print(extracted_url)
                m3u8_list.append(extracted_url)
            else:
                print("URL extraction failed.")
    print(m3u8_list)

    # 检测m3u8url是否有效，将有效url增加到列表
    valid_m3u8_link = []
    detectLinks(m3u8_list, name='浙江卫视')


