import requests
import re
from bs4 import BeautifulSoup
import os
import threading
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
    return m3u8_list


def download_m3u8(url):
    try:
        # 下载M3U8文件
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 检查请求是否成功
    except requests.exceptions.Timeout as e:
        print(f"{url}\nError: 请求超时. Exception: {e}")
    except requests.exceptions.RequestException as e:
        print(f"{url}\nError: 请求异常. Exception: {e}")
    else:
        m3u8_content = response.text
        # 解析M3U8文件，获取视频片段链接
        lines = m3u8_content.split('\n')
        segments = [line.strip() for line in lines if line and not line.startswith('#')]

        # 下载指定数量的视频片段并计算下载速度
        total_size = 0
        total_time = 0
        for i, segment in enumerate(segments[:3]):
            start_time = time.time()
            segment_url = url.rsplit('/', 1)[0] + '/' + segment
            response = requests.get(segment_url)
            end_time = time.time()

            # 将视频片段保存到本地
            with open('speed.ts', 'ab') as f:
                f.write(response.content)

            # 计算下载速度
            segment_size = len(response.content)
            segment_time = end_time - start_time
            segment_speed = segment_size / segment_time / (1024 * 1024)  # 转换为MB/s

            total_size += segment_size
            total_time += segment_time

            # print(f"Downloaded segment {i + 1}/3: {segment_speed:.2f} MB/s")

        # 计算平均下载速度
        average_speed = total_size / total_time / (1024 * 1024)  # 转换为MB/s
        print(f"Average Download Speed: {average_speed:.2f} MB/s")
        if average_speed >= 1:
            return url


def validate_m3u8_url(url, name):
    try:
        # 发送HTTP请求获取M3U8文件内容
        with requests.get(url, timeout=5) as response:
            response.raise_for_status()
            if response.status_code == 200:
                if download_m3u8(url):
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
    time.sleep(5)
    # 判断TV_names列表中的文件夹是否存在
    if not os.path.exists(f'{TV_name}'):
        os.makedirs(f'{TV_name}')
    with open(os.path.join(f'{TV_name}', f'{name}.txt'), 'w', encoding='utf-8') as file:
        for valid_url in valid_m3u8_link:
            file.write(f'{name},{valid_url}\n')
        print(f'-----{name}----有效源写入完成！！！------')
        valid_m3u8_link.clear()
        sys.stdout.flush()


def mer_links(tv):
    # 获取文件夹中的所有 txt 文件
    txt_files = [f for f in os.listdir(os.path.join(current_directory, f'{tv}'))]
    print(txt_files)
    # 打开合并后的文件，使用 'a' 模式以追加的方式写入
    with open(output_file_path, 'a', encoding='utf-8') as output_file:
        output_file.write(f'{tv},#genre#' + '\n')
        for txt_file in txt_files:
            # 拼接文件的完整路径
            file_path = os.path.join(os.path.join(current_directory, f'{tv}'), txt_file)

            # 打开当前 txt 文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as input_file:
                file_content = input_file.read()

                # 将当前 txt 文件的内容写入合并后的文件
                output_file.write(file_content)

                # 可以选择在每个文件之间加入换行，使合并后的内容更清晰
                output_file.write('\n')

    print(f'Merged content from {len(txt_files)} files into {output_file_path}')


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
    # TV_names = ['央视']
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
        mer_links(TV_name)
        tv_dict.clear()
    os.remove('speed.ts')
