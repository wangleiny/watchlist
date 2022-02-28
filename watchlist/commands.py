# -*- coding: utf-8 -*-
import click

from watchlist import app, db
from watchlist.models import User, Movie


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
    """Generate fake data."""
    db.create_all()

    name = 'Lei Wang'
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
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()

    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Admin')
        user.set_password(password)
        db.session.add(user)

    db.session.commit()
    click.echo('Done.')