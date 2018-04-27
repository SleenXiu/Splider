# coding=utf-8
# author:xsl

import os, sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, os.pardir)
sys.path.append(PROJECT_DIR)

import manager
from functools import wraps
from flask import Flask,url_for, redirect, render_template, session, jsonify
from flask_bootstrap import Bootstrap
from Splider.models import *
from forms import LoginForm, CreateSourceForm
from werkzeug.local import LocalProxy
from bson import ObjectId
from flask_login import login_required, login_user,LoginManager, AnonymousUserMixin, current_user

bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'

app = Flask(__name__)

app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'FDASGDASG'
app.config['TEMPLATES_AUTO_RELOAD'] = True

bootstrap.init_app(app)
login_manager.init_app(app)



@app.route('/')
@login_required
def index():
    return render_template('index.html')
    
@app.route('/post')
@login_required
def post():
    return render_template('post.html')

@app.route('/user')
@login_required
def user():
    return render_template('user.html')

@app.route('/source')
@login_required
def source():
    sources = Source.objects
    return render_template('source.html', sources=sources)


@app.route('/create_source', methods=['GET', 'POST'])
@login_required
def create_source():
    form = CreateSourceForm()
    form.type.choices = manager.SOURCE_TYPE
    if form.validate_on_submit():
        source = Source()
        source.name = form.name.data
        source.desc = form.desc.data
        source.url = form.url.data
        source.type = form.type.data
        source.extra = form.extra.data
        source.userid = current_user.id
        source.thirdid = form.thidrid.data
        source.save()
        return redirect('source')
    return render_template('create_source.html', form=form)

@app.route('/delete_source/<id>', methods=['POST'])
@login_required
def delete_source(id):
    s = Source.objects(id=ObjectId(id)).first()
    if s is not None:
        s.delete()
        return jsonify({'msg':'ok'})
    return jsonify({'msg':'not found'})


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        print('sdasads')
        if user is not None and user.check_password(form.password.data):
#            session['uid'] = str(user.id)
            login_user(user)
            print('5464')
            return redirect(url_for('index'))
        flash(u'无效的邮箱或密码')
    return render_template('login.html', form=form)

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=ObjectId(user_id)).first()

if __name__ == '__main__':
    app.run(debug=True)

