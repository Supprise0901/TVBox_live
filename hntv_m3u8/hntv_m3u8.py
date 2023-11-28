import json
import os

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构造上级目录的路径
parent_dir = os.path.dirname(current_dir)

# 要保存的文件名和内容
file_name = "hntv_m3u8.txt"

# 构造完整的文件路径
file_path = os.path.join(parent_dir, file_name)

# Assuming video_data.txt contains a JSON-formatted string
with open('video_data.txt', 'r', encoding='utf-8') as file:
    data_json = file.read()
    data = json.loads(data_json)

# Extracting name and video_streams values
with open(file_name, 'w') as f:
    f.write('河南地方,#genre#\n')
    for entry in data:
        name = entry.get("name", "")
        video_streams = entry.get("video_streams", "")
        print(f'{name},{video_streams[0]}')
        f.write(f'{name},{video_streams[0]}\n')


    # print(f"Name: {name}\nVideo Streams: {video_streams}\n")



