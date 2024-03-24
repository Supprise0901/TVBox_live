from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    with open('live.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    print(content)
    return render_template('index.html', content=content)


if __name__ == '__main__':
    app.run(host='192.168.3.12')
