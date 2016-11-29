#!/usr/bin/env python
# coding=utf-8
from alerta.api import ApiClient
from alerta.alert import Alert

api = ApiClient(endpoint='http://alert.localhost/api', key='UszE5hI_hx5pXKcsCP_2&1DIs&9_Ve*k')
#alert = Alert(resource='irdev', event='searchServerDown',text='The search server is down.',group='ir',environment="Production",service=["localhost"],status='open',timeout=86400,value="query1",severity="major")
alert = Alert(resource='irdev', event='searchServerDown',text='The search server is down.',group='ir',environment="Development",service=["localhost"],status='open',timeout=86400,value="query1",severity="major")
print alert
t = api.send(alert)
print t
