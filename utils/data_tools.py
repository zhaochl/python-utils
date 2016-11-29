#!/usr/bin/env python
# coding=utf-8
from data_util import *

def reset_table_field(table_name,field_name,value,limit=1000):
    sql =""
    if limit ==-1:
        sql ="select * from "+table_name+"";
    else:
        sql ="select * from "+table_name+" limit "+str(limit);
    results,coloum = DataUtil.db_query2('irweb','mydb',sql)
    print coloum,len(results)
    if len(results)==0:
        print " no data,not need to reset"
        exit(1)
    pk_name = coloum[0]
    pk_values = []
    if results!=None:
        for r in results:
            pk_value = r[0]
            pk_values.append(pk_value)
    pk_str = "("
    for _index,pv in enumerate(pk_values):
        pk_str+= str(pv)
        if _index<len(pk_values)-1:
            pk_str+=','
    pk_str+=")"
    #print pk_str
    sql_update = "update "+table_name+" set " +field_name+"="+value+" where "+pk_name+" in "+pk_str
    print sql_update
    DataUtil.db_update('irweb','mydb',sql_update)
    print "reset success"
def save_to_db_repeat(leads_name,title,url,fund,pubtime):
    sql = "select * from news_leads where leads_name='{0}' and title='{1}' and url='{2}' ;".format(leads_name,title,url)
    print sql
    
    check_results = False
    check_exist_results,coloum = DataUtil.db_query2('irweb','mydb',sql)
    print check_exist_results
    if check_exist_results!=None and len(check_exist_results)>0:
        check_results = True
        print 'exist'
    else:
        print 'not exist'

    now_str = get_today_str()
    status = 0
    sql = "insert into news_leads (leads_name,title,url,fund,create_time,pub_time,status) values('"+leads_name+"','"+title+"','"+url+"','"+fund+"','"+now_str+"','"+pubtime+"',"+str(status)+")"
    print sql
    if not check_results:
        DataUtil.db_update('irweb','mydb',sql)
        print 'insert ok'
def get_max_id():
    max_id = 0
    # find last update logId
    sql="select logId,userId,creationTime from search_query_log where userId!=0 and query!='' order by logId desc limit 1;"
    #print sql
    results = DataUtil.db_query('online','mydb',sql)
    if results!=None:
        for r in results:
            max_id = r[0]
            break
    return max_id
def get_min_id():
    min_id = 0
    # find last update logId
    sql="select logId,userId,creationTime from search_query_log where userId!=0 and query!='' order by logId desc limit 1;"
    #print sql
    results = DataUtil.db_query('online','mydb',sql)
    if results!=None:
        for r in results:
            min_id = r[0]
            break
    return min_id
"""
userlist = [1,2,3]
str =  '1,2,3'
usage: select * from a where id in('+str+')
"""

def convert_list_to_in_str(l):
    results =''
    if len(l)>0:
        for i,r in enumerate(l):
            results+=str(r)
            if i<len(l)-1:
                results+=','
    return results
if __name__=='__main__':
    ulist = [1,2,3,4]
    t = convert_list_to_in_str(ulist)
    print t


