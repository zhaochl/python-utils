#!/usr/bin/env python
# coding=utf-8
from db_util import *
from pdb import *
import logging
import logging.handlers

from datetime import datetime
from datetime import *
import time
import calendar

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
"""
demo:
    server='online'
    table='search_query_log'
    pk='logId'
    fields=['logId','query','sessionEnd','url','userId','creationTime']
    results =load_data_while(server,table,pk,fields,'asc',100000)
    
    all_limit =-1 means all data record
"""
def load_data_while(server,table,pk,fields,order='asc',all_limit=1000):
    
    lastId=0
    limit = 10000
    if limit > all_limit and all_limit!=-1:
        limit = all_limit/10
    results =None
    fields_str=''
    if fields!=None:
        if fields[0]!=pk:
            print 'fields[0] must be primary key'
            exit(1)
        fields_str=' , '.join(fields)
    else:
        fields_str = '*'
        print 'warn select * may result to I/O problem'
    order_tag = '>'
    if order=='asc':
        order_tag='>'
    elif order =='desc':
        order_tag='<'
    else:
        print 'wrong order option'
        exit(1)
    all_result = []
    count=0
    _order='asc'
    if order!=None and order!='':
        _order = order
    
    end=False
    loop_time=0
    while True:
        loop_time+=1
        sql="""
        select {}
        from {}
        where
        {} {} %s
        order by {} {} limit {};
        """.format(fields_str,table,pk,order_tag,pk,_order,str(limit))
        if loop_time==1:
            print 'load sql template:',sql
            logging.info('load_data_while start sql template:%s'%(sql))
        if end:
            logging.info('load_data ok,get to all_limit')
            break
        value_list=[lastId]
        results = None
        results = db_query(server,sql,value_list)
        if results!=None  and len(results)>0:
            for r in results:
                lastId=int(r[0])
                count+=1
                all_result.append(r)
                if len(all_result)==all_limit and all_limit!=-1:
                    end = True
                    break
        else:
            print ('load_data ok,over,count:%s'%(len(all_result)))
            break
        logging.info('loading_data table:%s,lastId:%s'%(table,str(lastId)))
    #//while true
    return all_result

"""
demo:
    server='online'
    table='search_query_log'
    pk='logId'
    fields=['logId','query','sessionEnd','url','userId','creationTime']
    results =load_data_while_recent_day(server,table,pk,fields,recent_day)
    
    all_limit =-1 means all data record
"""
def load_data_while_recent_day(server,table,pk,fields,recent_day=30,split_table_id_prefix=0):
    now_str = time.strftime("%Y-%m-%d %H:%M:%S")
    
    _d=(datetime.now() - timedelta(days = int(recent_day)))
    before_date = _d.strftime("%Y-%m-%d %H:%M:%S")
    print 'load data recent_day:'+str(recent_day)+',now:'+now_str+',before_date:'+str(before_date)
    
    max_id = _get_max_pk_value(server,table,pk)
    lastId = max_id
    limit = 10000
    order = 'desc'
    results =None
    fields_str=''
    if fields!=None:
        if fields[0]!=pk:
            print 'fields[0] must be primary key'
            exit(1)
        if fields[-1].lower().find('time')==-1:
            print 'fields[last] must like creationTime '
            exit(-1)
        fields_str=' , '.join(fields)
    else:
        fields_str = '*'
        print 'warn select * may result to I/O problem'
    order_tag = '>'
    if order=='asc':
        order_tag='>'
    elif order =='desc':
        order_tag='<'
    else:
        print 'wrong order option'
        exit(1)
    all_result = []
    count=0
    _order='asc'
    if order!=None and order!='':
        _order = order
    
    end=False
    loop_time=0
    while True:
        loop_time+=1
        sql="""
        select {}
        from {}
        where
        {} {} %s
        order by {} {} limit {};
        """.format(fields_str,table,pk,order_tag,pk,_order,str(limit))
        if loop_time==1:
            print 'load sql template:',sql
            logging.info('load_data_while start sql template:%s'%(sql))
        if end:
            logging.info('load_data ok,get to all_limit')
            break
        value_list=[lastId]
        results = None
        results = db_query(server,sql,value_list)
        if results!=None  and len(results)>0:
            for r in results:
                lastId=int(r[0])
                creationTime = str(r[-1])
                count+=1
                #----split table--
                if split_table_id_prefix!=0:
                    r = list(r)
                    r[0] += split_table_id_prefix
                    r=tuple(r)
                #------
                all_result.append(r)
                if creationTime < before_date:
                    end = True
                    break
        else:
            print ('load_data ok,over,count:%s'%(len(all_result)))
            break
        logging.info('loading_data table:%s,lastId:%s'%(table,str(lastId)))
    #//while true
    return all_result


def fix_month_str(m):
    m_str = str(m)
    if m<10:
        m_str = '0'+m_str
        return m_str
    else:
        return m_str
def get_before_months(recent_day):
    #now_ymd = time.strftime("%Y-%m-%d")
    #now_ymd_arr = now_ymd.split('-')
    #now_year  = now_ymd_arr[0]
    #now_month = now_ymd_arr[1]
    #now_day = now_ymd_arr[2]
    now_datetime = datetime.now()
    
    #print now_datetime
    now_year = now_datetime.year
    now_month = now_datetime.month
    #print now_month
    now_day = now_datetime.day
    #set_trace()
    now_year_month  = str(now_year) + fix_month_str(now_month)
    before_months = []
    
    now_month_range_tuple = calendar.monthrange(now_year,now_month)
    now_month_days_count = now_month_range_tuple[1]
    
    left = recent_day
    if left>now_day:
        left = left-now_day
        before_months.append([now_year_month,now_day])
    else:
        before_months.append([now_year_month,recent_day])
        return before_months


    before_month = now_month
    before_year = now_year
    while left>0:
        if before_month==1:
            before_month = 12
            before_year = before_year-1
        else:
            before_month = before_month-1
            before_year = before_year
        month_range_tuple = calendar.monthrange(before_year,before_month)
        month_days_count = month_range_tuple[1]
        before_year_month = str(before_year) + fix_month_str(before_month)
        
        left_new = left - month_days_count
        if left_new>0:
            before_months.append([before_year_month,month_days_count])
            left = left_new
        else:
            before_months.append([before_year_month,left])
            break
    return before_months
"""
demo:
def load_investor_app_log_data(recent_day):
    server='online_r'
    #table='investor_app_log_201609'
    table='investor_app_log'
    pk='logId'
    fields=['logId','userId','objectId','type','subtype','creationTime']
    #results =load_data_while_recent_day(server,table,pk,fields,recent_day)
    results =load_data_while_recent_day_split_table(server,table,pk,fields,recent_day)
    return results
"""
def load_data_while_recent_day_split_table(server,table_prifix,pk,fields,recent_day=30):
    merge_results = []
    before_months = get_before_months(recent_day)
    print before_months
    table = table_prifix
    for before_year_month,month_part_days  in before_months:
        split_table_id_prefix = int(before_year_month)*10000000
        if str(before_year_month)<'201608':
            table = table_prifix
        else:
            table = table_prifix+'_'+before_year_month
        print 'split month,before month:%s,part_days:%s,table:%s,id_prefix:%s'%(before_year_month,month_part_days,table,split_table_id_prefix)
        #continue

        split_table_results = load_data_while_recent_day(server,table,pk,fields,month_part_days,split_table_id_prefix)
        print 'load month:%s ok,count:%s'%(before_year_month,len(split_table_results))
        merge_results += split_table_results
    print 'load all split month ok,count:%s'%(len(merge_results))
    
    return merge_results
           
"""
demo:
    server='online'
    table='search_query_log'
    pk='logId'
    fields=['logId','query','sessionEnd','url','userId','creationTime']
    results =load_data_while(server,table,pk,fields,'asc',100000)
    
    all_limit =-1 means all data record
"""
def load_data_while_as_dict(server,table,pk,fields,order='asc',all_limit=1000):
    
    lastId=0
    limit = 10000
    if limit > all_limit and all_limit!=-1:
        limit = all_limit/10
    results = None
    fields_str=''
    if fields!=None:
        if fields[0]!=pk:
            print 'fields[0] must be primary key'
            exit(1)
        fields_str=' , '.join(fields)
    else:
        fields_str = '*'
        print 'warn select * may result to I/O problem'
    order_tag = '>'
    if order=='asc':
        order_tag='>'
    elif order_tag=='desc':
        order_tag='<'
    else:
        print 'wrong order option'
        exit(1)
    all_result = {}
    #all_result = []
    count=0
    _order='asc'
    if order!=None and order!='':
        _order = order
    
    end=False
    loop_time=0
    while True:
        loop_time+=1
        sql="""
        select {}
        from {}
        where
        {} {} %s
        order by {} {} limit {};
        """.format(fields_str,table,pk,order_tag,pk,_order,str(limit))
        if loop_time==1:
            print 'load sql template:',sql
            logging.info('load_data_while table:%s start sql template:%s'%(table,sql))
        if end:
            logging.info('load_data %s ok,get to all_limit'%(table))
            break
        value_list=[lastId]
        results = None
        results = db_query(server,sql,value_list)
        if results!=None  and len(results)>0:
            for r in results:
                lastId=int(r[0])
                count+=1
                #all_result.append(r)
                r = [str(x) for x in r]
                all_result[lastId] = r
                if len(all_result)==all_limit and all_limit!=-1:
                    end = True
                    break
        else:
            print ('load_data ok, table %s over,count:%s'%(table,len(all_result)))
            break
        logging.info('loading_data,lastId:'+str(lastId))
    #//while true
    return all_result
"""
SELECT `logId`  from `search_query_log` ORDER BY `logId` desc limit 1;
"""
def _get_max_pk_value(server,table,pk):
    max_id=0
    sql = "SELECT `%s`  from `%s` ORDER BY `%s` desc limit 1;"%(pk,table,pk)
    results = db_query(server,sql)
    if results!=None  and len(results)>0:
        for r in results:
            max_id = r[0]
            break
    return max_id
"""
return 201606
"""
def get_tomonth_str():
    _n= datetime.now()
    return _n.strftime("%Y%m")

def update_data_while(server,table,pk,data_dict,order='asc',all_limit=1000):
    
    lastId=0
    limit = 1000
    results =None
    fields = data_dict.keys()
    fields.insert(0,pk)
    fields_str=''
    if fields!=None:
        if fields[0]!=pk:
            print 'fields[0] must be primary key'
            exit(1)
        fields_str=' , '.join(fields)
    else:
        fields_str = '*'
        print 'warn: select * may result to I/O problem'
    all_result = []
    count=0
    _order='asc'
    if order!=None and order!='':
        _order = order
    
    end=False
    order_tag = '>'
    if order=='asc':
        order_tag='>'
    elif order_tag=='desc':
        order_tag='<'
    else:
        print 'wrong order option'
        exit(1)
    loop_time=0
    while True:
        loop_time+=1
        sql="""
        select {}
        from {}
        where
        {} {} %s
        order by {} {} limit {};
        """.format(fields_str,table,pk,order_tag,pk,_order,str(limit))
        
        if loop_time==1:
            logging.info('load_data_while start sql template:%s'%(sql))

        if end:
            logging.info('load_data ok,get to all_limit')
            break
        value_list=[lastId]
        results = None
        results = db_query(server,sql,value_list)
        if len(results)>1:
            for r in results:
                lastId=int(r[0])
                where_dict = {pk:lastId}
                db_update_data(server,table,data_dict,where_dict)
                count+=1
                all_result.append(r)
                if len(all_result)==all_limit:
                    end = True
                    break
        else:
            print ('load_data ok,over,count:%s'%(len(all_result)))
            break
        logging.info('loading_data,lastId:'+str(lastId))
    #//while true
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
    server='online_r'
    table='user'
    pk='userId'
    fields=['userId','name','company']
    #user_data = load_data_while(server,table,pk,fields)
    #user_data = load_data_while(server,table,pk,fields,'desc',3500)
    #print len(user_data)
    #max_id = _get_max_pk_value(server,table,pk)
    #print max_id

    table='search_query_log'
    pk='logId'
    data_dict = {'sessionEnd':'1'}
    where_str = " url!=''"
    order = 'asc'
    #update_data_while(server,table,pk,data_dict,order,where_str,1)
    t = get_before_months(100)
    print t
    #t = get_before_months(1)
    #print t
