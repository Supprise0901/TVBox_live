import json

# Assuming video_data.txt contains a JSON-formatted string
with open('video_data.txt', 'r', encoding='utf-8') as file:
    data_json = file.read()
    data = json.loads(data_json)

# Extracting name and video_streams values
with open('live.txt', 'w') as f:
    for entry in data:
        name = entry.get("name", "")
        video_streams = entry.get("video_streams", "")
        print(f'{name},{video_streams[0]}')
        f.write(f'{name},{video_streams[0]}\n')

    # print(f"Name: {name}\nVideo Streams: {video_streams}\n")
