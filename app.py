
import os
import sys
import click

from flask import Flask,flash,url_for,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash



WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')


db = SQLAlchemy(app)

login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user

login_manager.login_view = 'login'

@app.cli.command()
@click.option('--drop', is_flag=True, help='Create after drop.')
def initdb(drop):
    """Initialize the database."""
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
    

@app.cli.command()
@click.option('--username',prompt=True,help='The username used to login.')
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...') 
        user.username = username 
        user.set_password(password) # ????????????
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin') 
        user.set_password(password) # ???????????? 
        db.session.add(user)
    db.session.commit() # ????????????????????? 
    click.echo('Done.')


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20)) # ????????? 
    password_hash = db.Column(db.String(128)) # ???????????????
    
    def set_password(self, password): # ?????????????????????????????????????????? ????????????
        self.password_hash = generate_password_hash(password) # ???????????????????????????????????????
    def validate_password(self, password): # ????????????????????????????????? ?????????????????????
        return check_password_hash(self.password_hash, password) # ???????????????
    
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    mode = db.Column(db.String(100))

@app.context_processor
def inject_user():
    user = User.query.first()
    return dict(user=user)
@app.errorhandler(400)
def bad_request(e):
    return render_template('400.html'), 400
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST': # ??????????????? POST ??????
        # ??????????????????
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
    
        title = request.form.get('title') 
        mode = request.form.get('mode')
        # ????????????
        if not title or not mode or len(mode) > 30 or len(title) > 60:
            flash('Invalid input.') # ??????????????????
            return redirect(url_for('index')) # ?????????????????? # ??????????????????????????????
        movie = Movie(title=title, mode=mode) # ???????????? 
        db.session.add(movie) # ???????????????????????? 
        db.session.commit() # ?????????????????????
        flash('Item created.') # ??????????????????????????? 
        return redirect(url_for('index')) # ??????????????????
    #user = User.query.first()
    movies = Movie.query.all()
    #return render_template('index.html', user=user, movies=movies)
    return render_template('index.html', movies=movies)

    
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST': # ????????????????????????????????? 
        title = request.form['title']
        mode = request.form['mode']

        if not title or not mode or len(mode) > 30 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id)) # ?????????????????????????????????
        movie.title = title # ???????????? 
        movie.mode = mode # ???????????? 
        db.session.commit() # ????????????????????? 
        flash('Item updated.')
        return redirect(url_for('index')) # ??????????????????
    
    return render_template('edit.html', movie=movie) # ??????????????? ???????????????


@app.route('/movie/delete/<int:movie_id>', methods=['POST']) # ??????????????? POST ??????
@login_required # ????????????
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/home')
def home():
    return '<h1>????????????????????????!</h1>'

@app.route('/user/<name>')
def user_page(name):
    return '<h2>??????%s</h2>' % name+'<h2>?????????????????????</h2>'


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        
        if not name or len(name) > 60:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        
        user = User.query.first()
        user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    
    return render_template('settings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        
        user = User.query.first()
        
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))
        
        flash('Invalid username or password.')
        return redirect(url_for('login'))
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))

@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('home'))
    print(url_for('user_page',name='Wang Lei'))
    print(url_for('user_page',name='Juniper'))
    print(url_for('test_url_for'))
    print(url_for('test_url_for',num=2))
    return 'Test page!'


