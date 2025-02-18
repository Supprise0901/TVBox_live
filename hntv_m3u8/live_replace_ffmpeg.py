import os


def replace_content(live_file, live_ffmpeg_file, output_file):
    # 读取 live.txt 的内容
    with open(live_file, 'r', encoding='utf-8') as file:
        live_content = file.read()

    # 读取 live_ffmpeg.txt 的内容
    with open(live_ffmpeg_file, 'r', encoding='utf-8') as file:
        live_ffmpeg_content = file.read()

    # 找到需要替换的起始和结束位置
    start_marker = "热门卫视-体验"
    end_marker = "🇨🇳斗鱼电影,#genre#"

    start_index = live_content.find(start_marker)
    end_index = live_content.find(end_marker)

    # 如果找到起始和结束标记
    if start_index != -1 and end_index != -1:
        # 替换内容
        new_content = (
                live_content[:start_index]  # 保留起始标记之前的内容
                + live_ffmpeg_content  # 插入 live_ffmpeg.txt 的内容
                + live_content[end_index:]  # 保留结束标记之后的内容
        )
    else:
        print("未找到起始或结束标记，未进行替换。")
        new_content = live_content

    # 将新内容写入输出文件
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(new_content)

    print(f"替换完成，结果已保存到 {output_file}")


def main():
    # 文件路径
    # 获取当前脚本所在目录
    current_dir = os.getcwd()
    # 构造上级目录的路径
    parent_dir = os.path.dirname(current_dir)
    # 构造完整的文件路径
    live_file = os.path.join(parent_dir, "live.txt")
    # print(live_file)

    # run_speed_ffmpeg生成的live_ffmpeg.txt
    # live_ffmpeg_file = 'live_ffmpeg.txt'
    # mian生成的live.txt
    live_ffmpeg_file = 'live.txt'

    # 执行替换
    replace_content(live_file, live_ffmpeg_file, live_file)


if __name__ == "__main__":
    main()

