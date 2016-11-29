#!/usr/bin/env python
# coding=utf-8

from data_util import *
from redis_util import *
from mail_util import *

def check():
    print '--check--'
    projectIdList_all = DataUtil.get_project_list_cf_used()
    #print projectIdList_all
    pid_all_len = len(projectIdList_all)
    print 'all-count:',pid_all_len
    item_rec_results = get_json_to_hash_hash('item_rec_results_hash_hash')
    projectIdList_rec = item_rec_results.keys()
    pid_rec_len = len(item_rec_results.keys())
    #projectDetailDict = DataUtil.get_projects_infos_dict(projectIdList)
    print 'rec-count:',pid_rec_len
    projectIdList_rec_except =[]
    for pid in projectIdList_all:
        if pid not in projectIdList_rec and str(pid) not in projectIdList_rec:
            projectIdList_rec_except.append(pid)
    print 'rec except pids,len:',len(projectIdList_rec_except)
    coverage=0.0
    coverage = float(pid_rec_len)/float(pid_all_len)
    print 'coverage:',coverage
    
    # - fix add project 

    project_one_hour_new_dict ={}
    project_one_hour_new_dict = DataUtil.get_project_online_past('hor',1)

    #print projectIdList_rec_except
    # - save to redis - 
    key = 'itemcf_except_project_list'
    projectIdList_rec_except_old = get_list_verify(key)
    
    tag_has_new_exception = False
    print 'old:',projectIdList_rec_except_old
    for pid in projectIdList_rec_except:
        if pid not in projectIdList_rec_except_old and str(pid) not in projectIdList_rec_except_old:
            set_list_verify(key,pid)
            tag_has_new_exception = True
            print 'exception new pid more than 1 hour:',pid
        elif project_one_hour_new_dict.has_key(pid) or project_one_hour_new_dict.has_key(str(pid)):
            set_list_verify(key,pid)
            tag_has_new_exception = False
            print 'exception new pid in 1 hour:',pid
        else:
            tag_has_new_exception = False
    #select p.projectId,p.title,l.type,l.userId,u.name,u.company,l.localTime,p.status2 from investor_app_log l,project p,user u where l.type in ('APPLY_MEETING','COLLECT_PROJECT','PROJECT_VIEW','PROJECT_BP') and p.projectId = l.objectId  and u.userId=l.userId  and p.projectId in (11058, 11120, 14826, 17303) group by p.projectId order by l.logId;
    except_mail_info ="""
    <h2 class="section">New itemcf  Exceptions</h2>
    <p>recommend_project_total_total:{0},all_project_total:{1},coverage:{2}</p>
    <table cellpadding="5" cellspacing="0" border="1" bordercolor="#04B4AE" style="text-align: center; font-family: Arial; border-collapse: collapse; width: auto;">
    <tbody>
        <tr>
            <td colspan="8"><div>project itemcf exceptions</div></td>
        </tr>
        <tr>
            <th style="background-color: #04B4AE; color: #ffffff">projectID</th>
            <th style="background-color: #04B4AE; color: #ffffff">title</th>
            <th style="background-color: #04B4AE; color: #ffffff">status2</th>
            <th style="background-color: #04B4AE; color: #ffffff">userId</th>
            <th style="background-color: #04B4AE; color: #ffffff">username</th>
            <th style="background-color: #04B4AE; color: #ffffff">company</th>
            <th style="background-color: #04B4AE; color: #ffffff">type</th>
            <th style="background-color: #04B4AE; color: #ffffff">localTime</th>
        </tr>""".format(pid_rec_len,pid_all_len,coverage)
    #print except_mail_info
    results = DataUtil.get_project_list_to_verify(projectIdList_rec_except)
    if results !=None:
        for r in results:
            except_mail_info +="<tr>"
            projectId = r[0]
            title = r[1].strip().decode('utf-8','ignore')
            type = r[2].strip().decode('utf-8','ignore')
            userId = r[3]
            username = r[4].strip().decode('utf-8','ignore')
            company = r[5].strip().decode('utf-8','ignore')
            localTime = r[6]
            status2 = r[7]
            #print projectId,title,type,userId,username,company,localTime,status2
            except_mail_info+="<td>"+str(projectId)+"</td>"
            except_mail_info+="<td>"+title+"</td>"
            except_mail_info+="<td>"+str(status2)+"</td>"
            except_mail_info+="<td>"+str(userId)+"</td>"
            except_mail_info+="<td>"+username+"</td>"
            except_mail_info+="<td>"+company+"</td>"
            except_mail_info+="<td>"+type+"</td>"
            except_mail_info+="<td>"+localTime.strftime('%Y-%m-%d %H:%M:%S')+"</td>"
            except_mail_info +="</tr>"
    except_mail_info+="""
        </tbody>
        </table>
        <hr>
        """

    #toUserList = ['root@localhost.com']
    toUserList = ["root@localhost.com","houjianyu@localhost.com"]
    if tag_has_new_exception:
        sendmail('[monitor]search recommend itemcf exception','',toUserList,except_mail_info)
if __name__=='__main__':
    check()
