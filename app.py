from flask import Flask,url_for,render_template


name = "Lei Wang"

movies = [
    {'title':'金刚川','year':'2021'},
    {'title':'熊出没之重返地球','year':'2022'},
    {'title':'长津湖之水门桥','year':'2022'},
    {'title':'李茂换太子','year':'2022'},
    {'title':'四海','year':'2022'},
    {'title':'这个杀手不太冷静','year':'2022'},
    {'title':'狙击手','year':'2022'},
    {'title':'穿过寒冬拥抱你','year':'2022'},
    {'title':'奇迹.笨小孩','year':'2022'},
    {'title':'误杀2','year':'2022'},
    {'title':'跨过鸭绿江','year':'2022'},
]


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',name=name,movies=movies)

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