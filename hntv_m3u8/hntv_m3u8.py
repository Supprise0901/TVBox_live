import json
import os
import time

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构造上级目录的路径
parent_dir = os.path.dirname(current_dir)

# 构造完整的文件路径
file_path = os.path.join(parent_dir, "live.txt")

# Assuming video_data.txt contains a JSON-formatted string
with open('video_data.txt', 'r', encoding='utf-8') as file:
    data_json = file.read()
    data = json.loads(data_json)

# Extracting name and video_streams values
with open('live.txt', 'w', encoding='utf-8') as f:
    f.write('🇨🇳河南地方,#genre#\n')
    f.write('河南卫视,http://[2409:8087:7004:20:1000::22]:6610/yinhe/2/ch00000090990000001056/index.m3u8?virtualDomain=yinhe.live_hls.zte.com\n'
            '河南卫视,http://221.2.146.228:8888/newlive/live/hls/37/live.m3u8\n'
            '梨园频道,http://[2409:8087:4c0a:22:1::11]:6410/170000001115/UmaiCHAN6380788ba7bed/index.m3u8?AuthInfo=toEYVdLfxymUP2l9NZpQI5%2BK6T7j%2FlRm%2BvbM9VO7bA0q1S1k1f36SqqriM0FZoFSAJRfCt8SS7X6sTRmXb81a8O4H%2FdroDKjLoDeaMQdyJQ\n')
    for entry in data:
        name = entry.get("name", "")
        video_streams = entry.get("video_streams", "")
        print(f'{name},{video_streams[0]}')
        f.write(f'{name},{video_streams[0]}\n')

with open('live.txt', 'r', encoding='utf-8') as f:
    hntx_text = f.read()

with open('live_base.txt', 'r', encoding='utf-8') as f:
    base_text = f.read()

# 将新内容写入原始文本文件
with open(file_path, 'w', encoding='utf-8') as file:
    # content_text = hntx_text + '\n' + base_text
    content_text = base_text + '\n' + hntx_text
    file.write(content_text)

time.sleep(1)


