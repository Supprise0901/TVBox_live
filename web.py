import os
from flask import Flask, render_template

# 获取当前工作目录
base_dir = os.getcwd()
# print(base_dir)
TEMPLATES_DIR = os.path.join(base_dir, "templates")
# print(TEMPLATES_DIR)

# 创建 Flask 应用
app = Flask(__name__, template_folder=TEMPLATES_DIR)


@app.route('/')
def index():
    with open("live.txt", 'r', encoding='utf-8') as file:
        content = file.read()
    print(content)
    return render_template('index.html', content=content)


if __name__ == '__main__':
    print("请将直播源置于同一目录下，并命名为 live.txt")
    app.run(host='0.0.0.0', port=4545)
