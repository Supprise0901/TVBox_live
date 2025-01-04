import requests
from lxml import etree
import os
import threading
import time
import sys
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_url(name):
    user_agents = [
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Safari/537.36 Edg/116.0.1938.69',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6_3) AppleWebKit/537.36 (KHTML, like Gecko) Version/15.6 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Linux; Android 12; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Mobile Safari/537.36',
        'Mozilla/5.0 (Android 12; Mobile; rv:117.0) Gecko/117.0 Firefox/117.0',
        'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
        'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:117.0) Gecko/20100101 Firefox/117.0',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/116.0.5845.179 Chrome/116.0.5845.179 Safari/537.36',
        'Mozilla/5.0 (compatible; Konqueror/4.14; Linux) KHTML/4.14.2 (like Gecko)',
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Epiphany/42.3 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.179 Safari/537.36 OPR/103.0.4928.47",
    ]
    try:
        user_agent = random.choice(user_agents)
        # 配置ChromeOptions以启用无头模式
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={user_agent}")

        # 设置ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)

        # 创建Chrome WebDriver 实例
        # driver = webdriver.Chrome(options=options)

        # 打开指定页面
        driver.get('http://tonkiang.us/')

        username_input = driver.find_element(By.ID, 'search')
        username_input.send_keys(f'{name}')
        submit_button = driver.find_element(By.NAME, 'Submit')
        submit_button.click()

        # 获取页面的源代码
        page_source = driver.page_source

        # 打印源代码
        print(type(page_source))
        m3u8_list = []
        # 将 HTML 转换为 Element 对象
        root = etree.HTML(page_source)
        result_divs = root.xpath("//div[@class='resultplus']")
        print(f"搜索结果页数: {len(result_divs)}")
        # 打印提取到的 <div class="result"> 标签
        for div in result_divs:
            # 如果要获取标签内的文本内容
            # print(etree.tostring(div, pretty_print=True).decode())
            for element in div.xpath(".//tba"):
                if element.text is not None:
                    # m3u8_list.append(element.text.strip())
                    print(element.text.strip())
                    m3u8_list.append(element.text.strip())
                    with open('m3u8_list.txt', 'a', encoding='utf-8') as f:
                        f.write(f'{name},{element.text.strip()}' + '\n')

        # 关闭WebDriver
        driver.quit()
        return m3u8_list

    except requests.exceptions.RequestException as e:
        print(f"Error: 请求异常. Exception: {e}")
        return


def download_m3u8(url, name, initial_url=None):
    try:
        # 下载M3U8文件
        # with requests.get(url, timeout=10) as response:
        #     response.raise_for_status()
        response = requests.get(url, stream=True, timeout=15)
        response.raise_for_status()  # 检查请求是否成功
        m3u8_content = response.text
    except requests.exceptions.Timeout as e:
        print(f"{url}\nError: 请求超时. Exception: {e}")
        return
    except requests.exceptions.RequestException as e:
        print(f"{url}\nError: 请求异常. Exception: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return
    else:
        # 解析M3U8文件，获取视频片段链接
        lines = m3u8_content.split('\n')
        segments = [line.strip() for line in lines if line and not line.startswith('#')]
        if len(segments) == 1:
            # 在递归调用时传递 initial_url 参数
            return download_m3u8(segments[0], name, initial_url=initial_url if initial_url is not None else url)

        # 下载指定数量的视频片段并计算下载速度
        total_size = 0
        total_time = 0
        for i, segment in enumerate(segments[:3]):
            start_time = time.time()
            segment_url = url.rsplit('/', 1)[0] + '/' + segment
            response = requests.get(segment_url)
            end_time = time.time()

            # 将视频片段保存到本地
            with open('video.ts', 'wb') as f:
                f.write(response.content)

            # 计算下载速度
            segment_size = len(response.content)
            segment_time = end_time - start_time
            segment_speed = segment_size / segment_time / (1024 * 1024)  # 转换为MB/s

            total_size += segment_size
            total_time += segment_time

            print(f"Downloaded segment {i + 1}/3: {segment_speed:.2f} MB/s")

        # 计算平均下载速度
        average_speed = total_size / total_time / (1024 * 1024)  # 转换为MB/s
        print(f"---{name}---Average Download Speed: {average_speed:.2f} MB/s")
        # print(f"---{name}---平均速度: {average_speed:.2f} MB/s")

        # 速度阈值，默认1MB/s
        if average_speed >= speed:
            valid_url = initial_url if initial_url is not None else url
            # if not os.path.exists(f'{name}'):
            #     os.makedirs(f'{name}')
            with open('Single_live.txt', 'a', encoding='utf-8') as file:
                file.write(f'{name},{valid_url}\n')
            print(f"---{name}---链接有效源已保存---\n"
                  f"----{valid_url}---")
            return


def detectLinks(name, m3u8_list):
    thread = []
    for m3u8_url in m3u8_list:
        t = threading.Thread(target=download_m3u8, args=(m3u8_url, name,))
        t.daemon = True  # 设置为守护线程,确保在主线程退出时，所有子线程都会被强制终止
        t.start()
        thread.append(t)
    # 等待所有线程完成
    for t in thread:
        try:
            print(f"Waiting for thread {t} to finish")
            t.join(timeout=10)  # 等待线程超时
        except Exception as e:
            print(f"Thread {t.name} raised an exception: {e}")


def re_dup(filepath):
    from collections import OrderedDict
    # 读取文本文件
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    # 保持原始顺序的去重
    unique_lines_ordered = list(OrderedDict.fromkeys(lines))
    # 将去重后的内容写回文件
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(unique_lines_ordered)
    print('-----直播源去重完成！------')


if __name__ == '__main__':
    # 下载速度阈值，默认1MB/s
    speed = 1
    # 获取当前工作目录
    current_directory = os.getcwd()
    output_file_path = os.path.join(current_directory, 'Single_live.txt')
    # 清空live.txt内容
    with open(output_file_path, 'w', encoding='utf-8') as f:
        pass
    tv_dict = {}
    # 输入要搜索的直播源名称
    name = input('请输入要搜索的直播源名称：')
    # 调用get_url函数获取直播源m3u8链接
    m3u8_list = get_url(name)
    tv_dict[name] = m3u8_list
    print(name)
    print('---------字典加载完成！------------')
    for name, m3u8_list in tv_dict.items():
        detectLinks(name, m3u8_list)
    # 合并有效直播源m3u8链接
    tv_dict.clear()
    time.sleep(10)
    try:
        os.remove('video.ts')
        print('-----清理临时文件完成！------')

    except Exception as e:
        pass
    # 直播源去重
    re_dup(output_file_path)

    sys.exit()
