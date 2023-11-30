import os

# 获取当前工作目录
current_directory = os.getcwd()

# 设置合并后的文件路径
output_file_path = os.path.join(current_directory, 'live.txt')


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
