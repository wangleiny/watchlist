
import os
import sys
import click

from flask import Flask,url_for,render_template
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prifix ='sqlite:///'
else:
    prefix = 'sqlite:////'
    


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

    
@app.cli.command()
@click.option('--drop',is_flag=True,help='Create after drop.')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')
    
@app.cli.command()    
def forge():
    db.create_all()
    name = "Juniper"
    
    movies = [
        {'title':'MX路由器-运营商款','mode':'MX2020/2010/2008'},
        {'title':'MX路由器-DC款','mode':'MX10016/10008/10004/10003'},
        {'title':'MX路由器-经典款','mode':'MX960/480/240'},
        {'title':'MX路由器-边缘接入款','mode':'MX304/204/150/104'},
        
        {'title':'QFX DC交换机-Spine系列1','mode':'QFX100016/10008/10002'},
        {'title':'QFX DC交换机-Spine系列2','mode':'QFX5700/5130/5220/5210'},
        {'title':'QFX DC交换机-Leaf系列','mode':'QFX5110/5120'},
        
        {'title':'EX 园区网交换机-核心层','mode':'EX9214/9208/9204/9250'},
        {'title':'EX 园区网交换机-汇聚层','mode':'EX4650/4600/4400/4300'},
        {'title':'EX 园区网交换机-接入层','mode':'EX4300/2300'},
        
        {'title':'SRX防火墙-运营商级别','mode':'SRX5800/5600/5400'},
        {'title':'SRX防火墙-DC级别','mode':'SRX4600/4200/4100/1500'},
        {'title':'SRX防火墙-企业级别','mode':'SRX550/380/345/340/320/300'},
        
        {'title':'Mist无线-室内款','mode':'AP43/41/33/32/12'},
        {'title':'Mist无线-室外款','mode':'AP63/61'},
        
        
    ]
    
    
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], mode=m['mode'])
        db.session.add(movie)
        
    db.session.commit()
    click.echo('Done.')


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(60))
    mode = db.Column(db.String(40))

@app.route('/')
def index():
    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html',user=user,movies=movies)

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


