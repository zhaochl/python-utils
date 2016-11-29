#!/usr/bin/env python
# coding=utf-8

from http_util import *
from data_util import *
from redis_util import *
from text_util import *
from mail_util import *
from alert_util import *
import json
import urllib2 
from urllib import urlencode
from urllib import quote
import time
from pdb import *
alert_title = ""

def check_http_service_avaiable(keyword):
    
    #keyword =  quote(keyword.encode('utf8'))
    #set_trace()
    keyword_old = keyword
    keyword = keyword.encode('utf8')
    _status=False
    #host = 'localhost'
    host = 'localhost'
    #print keyword
    param = {
        'query':keyword,
        'bejson':'1',
        'intersect':'1'
    }
    #url ="http://"+host+"/search?query="+keyword+"&bejson=1&crs=1&pagesize=200&t=1457509108000&intersect=1"
    url ="http://"+host+"/search?"+urlencode(param)
    print keyword,url
    #exit(1)
    results = get_json_from_url(url)
    time.sleep(2)
    #print results
    totalcount = results['totalcount']
    pl_list = results['pl_list']
    print url,'totalcount:',totalcount,',pl_list:',len(pl_list)
    global alert_title
    alert_title="keyword:"+str(keyword_old)+",url:"+url+",totalcount:"+str(totalcount)+",len-pl_list:"+str(len(pl_list))
    if totalcount !=None and int(totalcount) >0 and len(pl_list)>0:
        _status = True
    else:
        print  "bad :",results
        print results
    return _status

def check_search_service_all(hor):
    recentProjectDict = DataUtil.get_project_online_past('hor',hor)
    if len(recentProjectDict)==0:
        print 'no new project at '+get_today_str()
        return
    #print recentProjectDict
    # - save to redis - 
    key = 'search_service_except_project_list'
    projectIdList_rec_except_old = []
    #projectIdList_rec_except_old = get_list_verify(key)
    
    except_mail_info ="""
    <h2 class="section">New search interface available  Exceptions</h2>
    <p class="section">提示:如果没有异常，该邮件不会出现</p>
    <table cellpadding="5" cellspacing="0" border="1" bordercolor="#04B4AE" style="text-align: center; font-family: Arial; border-collapse: collapse; width: auto;">
    <tbody>
        <tr>
            <td colspan="3"><div>project search exceptions</div></td>
        </tr>
        <tr>
            <th style="background-color: #04B4AE; color: #ffffff">projectID</th>
            <th style="background-color: #04B4AE; color: #ffffff">title</th>
            <th style="background-color: #04B4AE; color: #ffffff">search status</th>
        </tr>"""

    tag_has_new_exception = False
    for pid,ptitle in recentProjectDict.iteritems():
        #print 'pid:',pid,',ptitle:',ptitle
        search_info = ""
        if ptitle !="" and not has_abnormal_char(ptitle):
        #if pid not in projectIdList_rec_except_old and str(pid) not in projectIdList_rec_except_old:
            print 'find a new project,pid:',pid,',title:',ptitle
            ptitle = ptitle.lower()
            status = check_http_service_avaiable(ptitle)

            #alert_title = 'pid:'+str(pid)+',ptitle:'+ptitle
            if  status:
                search_info="<font color=green>ok</font>"
            else:
                search_info="<font color=red>oops!</font>"
                tag_has_new_exception = True
        
            if tag_has_new_exception:
                tag_has_new_exception = True
                except_mail_info +="<tr>"
                except_mail_info+="<td>"+str(pid)+"</td>"
                except_mail_info+="<td>"+ptitle+"</td>"
                except_mail_info+="<td>"+search_info+"</td>"
                except_mail_info +="</tr>"
            #set_list_verify(key,pid)
    except_mail_info+="""
        </tbody>
        </table>
        <hr>
        """
    toUserList = ['root@localhost.com']
    #toUserList = ["root@localhost.com","houjianyu@localhost.com","yandechen@localhost.com"]
    #toUserList = ["root@localhost.com","houjianyu@localhost.com"]
    if tag_has_new_exception:
        sendmail('[monitor]search search service available exception','',toUserList,except_mail_info)
    
        alert('irdev','monitor_search','search_service_error',alert_title,'critical','open',True)
    else:
        alert('irdev','monitor_search','crontab run success',alert_title,'normal','open',True)
    today = get_today_str()
    print 'runs success at '+today
    return tag_has_new_exception
if __name__=='__main__':
    #check()
    is_sendmail = False
    #for h in [1,2,4,8]:
    for h in [3]:
        is_sendmail =check_http_service_avaiable(h)
        if is_sendmail:
            print '---sendmail'
            break
    time.sleep(1)
    #k="护礼家1"
    #t=check_search_service_avaiable(k)
    #print t
