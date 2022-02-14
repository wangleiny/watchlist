
import os
import sys
import click

from flask import Flask,flash,url_for,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:
    prifix ='sqlite:///'
else:
    prefix = 'sqlite:////'
    


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'DEV'

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
        {'title':'MX Router-SP','mode':'MX2020/2010/2008'},
        {'title':'MX Router-DC','mode':'MX10016/10008/10004/10003'},
        {'title':'MX Router-Core','mode':'MX960/480/240'},
        {'title':'MX Router-Edge','mode':'MX304/204/150/104'},
        
        {'title':'QFX DC Switch-Spine1','mode':'QFX100016/10008/10002'},
        {'title':'QFX DC Switch-Spine2','mode':'QFX5700/5130/5220/5210'},
        {'title':'QFX DC Switch-Leaf','mode':'QFX5110/5120'},
        
        {'title':'EX Campus Switch-Core','mode':'EX9214/9208/9204/9250'},
        {'title':'EX Campus Switch-Aggregation','mode':'EX4650/4600/4400/4300'},
        {'title':'EX Campus Switch-Access','mode':'EX4300/2300'},
        
        {'title':'SRXFirewall-SP','mode':'SRX5800/5600/5400'},
        {'title':'SRXFirewall-DC','mode':'SRX4600/4200/4100/1500'},
        {'title':'SRXFirewall-Edge','mode':'SRX550/380/345/340/320/300'},
        
        {'title':'Mist AP-indoor','mode':'AP43/41/33/32/12'},
        {'title':'Mist AP-outdoor','mode':'AP63/61'},
        
        
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

    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title') 
        mode = request.form.get('mode')
        # 验证数据
        if not title or not mode or len(mode) > 30 or len(title) > 60:
            flash('Invalid input.') # 显示错误提示
            return redirect(url_for('index')) # 重定向回主页 # 保存表单数据到数据库
        movie = Movie(title=title, mode=mode) # 创建记录 
        db.session.add(movie) # 添加到数据库会话 
        db.session.commit() # 提交数据库会话
        flash('Item created.') # 显示成功创建的提示 
        return redirect(url_for('index')) # 重定向回主页
    #user = User.query.first()
    movies = Movie.query.all()
    #return render_template('index.html', user=user, movies=movies)
    return render_template('index.html', movies=movies)



@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # 处理编辑表单的提交请求 
        title = request.form['title']
        mode = request.form['mode']

        if not title or not mode or len(mode) > 30 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id)) # 重定向回对应的编辑页面
        movie.title = title # 更新标题 
        movie.mode = mode # 更新年份 
        db.session.commit() # 提交数据库会话 
        flash('Item updated.')
        return redirect(url_for('index')) # 重定向回主页
    
    return render_template('edit.html', movie=movie) # 传入被编辑 的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST']) # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id) # 获取电影记录 
    db.session.delete(movie) # 删除对应的记录 
    db.session.commit() # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index')) # 重定向回主页



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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)