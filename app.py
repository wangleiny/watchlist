from flask import Flask,url_for

app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>欢迎来到我的世界!</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/index')
@app.route('/home')
def home():
    return '<h1>欢迎来到我的主页!</h1>'

@app.route('/user/<name>')
def user_page(name):
    return '<h2>欢迎%s</h2>' % name+'<h2>来到我的世界！</h2>'


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('home'))
    print(url_for('user_page',name='Wang Lei'))
    print(url_for('user_page',name='Juniper'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=2))
    return 'Test page!'