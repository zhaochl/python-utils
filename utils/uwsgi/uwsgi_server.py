#!/usr/bin/env python
# coding=utf-8
#pip install uwsgi
# test.py
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    return "Hello uwsgi"


