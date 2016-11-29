#!/usr/bin/env python
# coding=utf-8
from alerta.api import ApiClient
from alerta.alert import Alert

alert_title=""
"""
---severity----
Severity    Severity Code   Colour
critical    1   Red
major   2   Orange
minor   3   Yellow
warning 4   Blue
indeterminate   5   Green
cleared 5   Green
normal  5   Green
ok  5   Green
informational   6   Green
debug   7   Purple
security    8   Grey
unknown 9   Grey
---status--
Status  Status Code
open    1
assign  2
ack 3
closed  4
expired 5
unknown 9
"""
def alert_rawData(resource,event,text,value,rawData,severity,status,go=False):
    api = ApiClient(endpoint='http://alert.localhost/api', key='UszE5hI_hx5pXKcsCP_2&1DIs&9_Ve*k')
    #alert = Alert(resource='irdev', event='searchServerDown',text='The search server is down.',group='ir',environment="Production",service=["localhost"],status='open',timeout=86400,value="query1",severity="major")
    #alert = Alert(resource='irdev', event='searchServerDown',text='The search server is down.',group='ir',environment="Development",service=["localhost"],status='open',timeout=86400,value="query1",severity="major")
    #2h expired
    alert_info = Alert(resource=resource, event=event,text=text,rawData=rawData,group='ir',environment="Production",service=["localhost"],status=status,timeout='2880',value=value,severity=severity)
    t = api.send(alert_info)
    if not go:
        print 'alert info:',alert_info
        print t
def alert(resource,event,text,value,severity,status,go=False):
    api = ApiClient(endpoint='http://alert.localhost/api', key='UszE5hI_hx5pXKcsCP_2&1DIs&9_Ve*k')
    #2h expired
    alert_info = Alert(resource=resource, event=event,text=text,group='ir',environment="Production",service=["localhost"],status=status,timeout='2880',value=value,severity=severity)
    t = api.send(alert_info)
    if not go:
        print 'alert info:',alert_info
        print t
   
if __name__=='__main__':
    #use tpl
    
    #global alert_title
    #alert_title="keyword:"+str(keyword_old)+",url:"+url+",totalcount:"+str(totalcount)
    alert_title="demo - title,set text or data want to show."
    error = False
    if error:
        alert('demo','monitor_search','search_service_error',alert_title,'critical','open',True)
    else:
        alert('demo','monitor_search','crontab run success',alert_title,'normal','open',True)
