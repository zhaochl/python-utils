#!/usr/bin/env python
# coding=utf-8
from db_util import *
from pdb import *
#return 
"""
{1: 
    {
    1: [[1, 'view', '10:21'], [9, 'click', '10:21']], 
    2: [[5, 'click', '10:23']]
    }
}
"""
def build_log_hash_hash(logs,allow_repeat=False):
    
    #{uid:{pid:[]}}
    user_project_action = {}
    for r in logs:
        logid = r[0]
        userid = r[1]
        projectId = r[2]
        action = r[3]
        creationTime = r[4]
        item = [logid,action,creationTime]
        if not user_project_action.has_key(userid):
            user_project_action[userid] = {projectId:[item]} 
        else:
            old_projectId_dict = user_project_action[userid]
            if not old_projectId_dict.has_key(projectId):
                old_projectId_dict[projectId] = [item]
            else:
                if allow_repeat:
                    old_projectId_dict[projectId].append(item)
                else:
                    exist = False
                    for log in old_projectId_dict[projectId]:
                        #action
                        if log[1] == item[1]:
                            exist=True
                            break
                    if not exist:
                        old_projectId_dict[projectId].append(item)
            user_project_action[userid] = old_projectId_dict
    return user_project_action
def search_log_hash(user_project_action,userid,projectId=None):
    result = None
    if user_project_action.has_key(userid):
        userid_dict = user_project_action[userid]
        if projectId==None:
            result = userid_dict
        else:
            if userid_dict.has_key(projectId):
                result = userid_dict[projectId]
    return result

def load_data_while(server,table,pk,fields):
    
    lastId=0
    limit = 1000
    results =None
    fields_str=''
    if fields!=None:
        if fields[0]!=pk:
            print 'fields[0] must be primary key'
            exit(1)
        fields_str=' , '.join(fields)
    else:
        fields_str = '*'
        print 'waring select * may result to I/O problem'
    all_result = []
    count=0
    while True:
        sql="""
        select {}
        from {}
        where
        {}>%s
        order by {} asc limit {};
        """.format(fields_str,table,pk,pk,str(limit))
        
        value_list=[lastId]
        results = None
        results = db_query(server,sql,value_list)
        if len(results)>1:
            for r in results:
                lastId=int(r[0])
                count+=1
                all_result.append(r)
        else:
            print ('load_data end.')
            break
    #//while true
    print 'count:',count
    return all_result
def t():
    sql="""
    SELECT name from user where `userId` =%s;
    """
    value_list=['1']
    results = db_query('online',sql,value_list)
    print results

def test_build_log_hash():
    #init_all_project_user_score_cache()
    #load_investor_app_log()
    #loigid,uid,pid,action,time
    logs=(
        (1,1,1,'view','10:21'),
        (2,2,2,'view','8:10'),
        (3,2,1,'click','9:10'),
        (4,2,3,'click','10:22'),
        (5,1,2,'click','10:23'),
        (6,3,1,'view','10:30'),
        (7,3,1,'view','10:21'),
        (8,3,2,'view','10:22'),
        (9,1,1,'click','10:21'),
    )
    user_project_action = build_log_hash_hash(logs)
    print user_project_action
    logs = search_log_hash(user_project_action,1,1)
    print logs

if __name__=='__main__':
    #t()
    server='online'
    table='user'
    pk='userId'
    fields=['userId','name','company']
    user_data = load_data_while(server,table,pk,fields)
    print len(user_data)
