#!/usr/bin/env python
# coding=utf-8
# author: xsl

from flask import Flask, jsonify, request
import json

app = Flask(__name__)

f = open('weibo/yifa.json', 'r')
data = f.read()

@app.route('/weibo')
def weibo():
    page = request.args.get('page', 0, type=int)
    count = request.args.get('count', 20, type=int)
    blogs = json.loads(data)
    res = blogs[page*count:page*count+count]
    return jsonify(res)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)

