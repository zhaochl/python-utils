#!/usr/bin/env python
# coding=utf-8

from data_util import *
from redis_util import *
from mail_util import *
import json
import urllib2 
def check_cf_interface_by_projectId(projectId):
    _status=False
    #projectId = '17855'
    host = 'localhost'
    #req = urllib2.Request('http://'+host+'/usercf?userid=3&projectid=17855&bejson=1') 
    try:
        req = urllib2.Request('http://'+host+'/usercf?userid=3&projectid='+projectId+'&bejson=1') 
        response = urllib2.urlopen(req) 
        the_page = response.read()
        #print the_page
        json_result = json.loads(the_page)
        totalcount =  json_result['totalcount']
        if totalcount !=None and int(totalcount) >0:
            _status = True
    except:
        print 'error,projectId:',projectId
    return _status
def check_cf_interface_all():
    recentProjectDict = DataUtil.get_project_online_past('day',1)
    illegal_project_list = DataUtil.get_project_illegal()
    #print illegal_project_list

    # - save to redis - 
    key = 'itemcf_interface_except_project_list'
    projectIdList_rec_except_old = []
    projectIdList_rec_except_old = get_list_verify(key)
    
    except_mail_info ="""
    <h2 class="section">New interface available  Exceptions</h2>
    <table cellpadding="5" cellspacing="0" border="1" bordercolor="#04B4AE" style="text-align: center; font-family: Arial; border-collapse: collapse; width: auto;">
    <tbody>
        <tr>
            <td colspan="8"><div>project itemcf exceptions</div></td>
        </tr>
        <tr>
            <th style="background-color: #04B4AE; color: #ffffff">projectID</th>
            <th style="background-color: #04B4AE; color: #ffffff">title</th>
        </tr>"""

    tag_has_new_exception = False
    for pid,ptitle in recentProjectDict.iteritems():
        #print 'pid:',pid,',ptitle:',ptitle

        if pid not in projectIdList_rec_except_old and str(pid) not in projectIdList_rec_except_old:
            if pid not in illegal_project_list:
                print 'find a new project,pid:',pid
                status = check_cf_interface_by_projectId(int(pid))
                if not status:
                    tag_has_new_exception = True
                    except_mail_info +="<tr>"
                    except_mail_info+="<td>"+str(pid)+"</td>"
                    except_mail_info+="<td>"+ptitle+"</td>"
                    except_mail_info +="</tr>"
                set_list_verify(key,pid)
    except_mail_info+="""
        </tbody>
        </table>
        <hr>
        """
    #toUserList = ['root@localhost.com']
    toUserList = ["root@localhost.com","houjianyu@localhost.com"]
    if tag_has_new_exception:
        sendmail('[monitor]search recommend interface available exception','',toUserList,except_mail_info)

    today = get_today_str()
    print 'runs success at '+today
if __name__=='__main__':
    #check()
    check_cf_interface_all()
