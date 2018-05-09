#coding=utf-8
# author:xsl

import os, sys
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_DIR = os.path.join(CURRENT_DIR, os.pardir)
sys.path.append(PROJECT_DIR)

from mongoengine.queryset import QuerySet
import manager
from functools import wraps
from flask import Flask,request,flash,url_for, redirect, render_template, session, jsonify
from flask_bootstrap import Bootstrap
from Splider.models import *
from forms import CreateUserForm, LoginForm, EditUserForm, CreateSourceForm
from werkzeug.local import LocalProxy
from bson import ObjectId
from flask_login import (
        login_required, 
        login_user,
        LoginManager, 
        AnonymousUserMixin, 
        current_user,
        logout_user,
    )

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



from user import user as user_blueprint
app.register_blueprint(user_blueprint, url_prefix='/user')


@app.route('/')
@login_required
def index():
    return render_template('index.html')
    
@app.route('/post')
@login_required
def post():
    page = request.args.get("page") or 0
    page = int(page)
    all_posts = Post.objects
    posts = all_posts[page*20:page*20+20]
    return render_template('post.html', posts=posts, pages=int(len(all_posts)/20), page=page)

@app.route('/users')
@login_required
def users():
    users = User.objects
    return render_template('user.html', users=users)

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


@app.route('/user/create', methods=['GET', 'POST'])
@login_required
def user_create():
    form = CreateUserForm()
    if form.validate_on_submit():
        u = User()
        u.name = form.name.data
        u.third_id = form.third_id.data
        u.third_type = form.third_type.data
        u.email = form.email.data
        u.password = form.password.data
        u.phone = form.phone.data
        u.type = form.type.data
        u.save()
        return redirect(url_for('user.index'))
    return render_template('user_create.html', form=form)

@app.route('/user/edit', methods=['GET','POST'])
@login_required
def user_edit():
    form = EditUserForm()
    if form.validate_on_submit():
        name = form.name.data
        avatar = form.avatar.data
        if len(name) > 0:
            current_user.name = name
        if len(avatar) > 0:
            current_user.avatar = avatar
        current_user.save()
        flash('edit ok')
        return redirect(url_for('index'))
    return render_template('edit_user.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            print('5464')
            return redirect(url_for('index'))
        flash(u'无效的邮箱或密码')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))



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

