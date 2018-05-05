# coding=utf-8
# author:xsl

from . import user
from Splider.models import *
from Splider.weibo import *
from flask import render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required
from bson import ObjectId
from .forms import *

@user.route('/')
def index():
    users = User.objects()
    return render_template('user.html', users=users)

@user.route('/reset')
def reset():
    u = User.objects(email='xsl@ins.com').first()
    u.password = 'xiushilin'
    u.save()
    return jsonify({"msg":"ok"})

@user.route('/delete', methods=['POST'])
@login_required
def delete():
    id = request.json.get('id')
    u = User.objects(id=ObjectId(id)).first()
    if u is not None:
        u.delete()
        return jsonify({'msg':'ok'})
    return jsonify({'msg':'not found'})

@user.route('/create', methods=['POST'])
@login_required
def create():
    tid = request.json.get('tid')
    name = request.json.get('name')
    avatar = request.json.get('avatar')
    type = request.json.get('type')
    u = User()
    u.third_id = str(tid)
    print(tid)
    u.name = name
# need download avatar
    u.avatar = avatar
    u.type = type
    u.save()
    return jsonify({'msg':'ok'})

@user.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    id = request.args.get('id')
    u = User.objects(id=ObjectId(id)).first()
    if u is not None:
        form = EditUserForm()
        form.name.data = u.name
        form.avatar.data = str(u.avatar)
        form.phone.data = u.phone
        form.email.data = u.email
        form.password.data = u.password
        form.type.data = u.type

        if form.validate_on_submit():
            name = form.name.raw_data[0]
            avatar = form.avatar.raw_data[0]
            type = form.type.raw_data[0]
            print(form.name.object_data)
            if len(name) > 0:
                u.name = name
            if len(avatar) > 0:
                u.avatar = avatar
            if len(type) > 0:
                u.type = type
            u.save()
            flash('edit ok')
            return redirect(url_for('user.index'))
        return render_template('edit_user.html', form=form)
    flash('user not found')
    return redirect(url_for('user.index'))

@user.route('/weibo')
@login_required
def weibo():
    return render_template('user_weibo.html')

@user.route('/weibo_search', methods=['POST'])
@login_required
def weibo_search():
    name = request.json.get('name') or ""
    sp = WeiboSplider()
    cards = sp.search_user_list(name)
    users = []
    for card in cards:
        user = card.get('user')
        users.append(user)
    return jsonify(users)

