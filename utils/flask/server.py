#!/usr/bin/env python
# coding=utf-8

from flask import Flask
from flask import *

from functools import wraps
from flask import make_response

app = Flask(__name__)
"""
def allow_cross_domain(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        rst = make_response(fun(*args, **kwargs))
        rst.headers['Access-Control-Allow-Origin'] = '*'
        rst.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        rst.headers['Access-Control-Allow-Headers'] = allow_headers
        return rst
    return wrapper_fun

@app.route('/jsonp')
@allow_cross_domain
def domains():
    json_result = {}    
    json_result['pl_list'] = 'test'
    resp = make_response(json.dumps(json_result))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    resp.headers['Content-Type'] = "application/json"
    return resp
    
"""

@app.route('/')
def hello_world():
    return 'Hello <font color=red>flask!</font>'

@app.route('/index')
def index(name=None):
    s = '医疗'
    #results = query_sentence(s)
    #results = query_sentence(s)
    return render_template('index.html', name=name)
@app.route('/search/<keyword>')
def search(keyword):
    print 'query keyword:',keyword
    keyword = keyword.encode('utf8')
    json_result = {}    
    json_result['pl_list'] = 'test'
    resp = make_response(json.dumps(json_result))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    resp.headers['Content-Type'] = "application/json"
    return resp

@app.route('/api/searchlog',methods=['GET','POST'])
def searchapi():
    json_result={}
    resp = make_response(json.dumps(json_result))
    resp.headers['Access-Control-Allow-Origin'] = "*"
    resp.headers['Content-Type'] = "application/json"
    return resp
    
if __name__ == '__main__':
    app.debug = True
    print 'server is running at 1111'
    app.run(host='0.0.0.0',port=1111,threaded=True)
