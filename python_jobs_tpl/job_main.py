#!/usr/bin/env python
# coding=utf-8
from data_util import *
from date_util import *
from redis_util import *
from alert_util import *
import sys
rkey ="job_key"

alert_title = ""
def job_process_break_point(go=False):
    break_id =0
    break_id_new=0
    break_id = get_string(rkey)
    if break_id==None:
        break_id=0
    else:
        break_id_new = break_id
    sql="select aid,title,url,addtime,pubtime from doc_tab where aid>"+str(break_id)+" and (dupe_ids is null or dupe_ids = '') order by aid asc limit 1000;"
    print sql
    results,c = DataUtil.db_query2('irweb','mydb',sql)
    print 'count:',len(results)
    for r in results:
        aid = r[0]
        break_id_new =  aid
    if go:
        set_string(rkey,break_id_new)

def job_process_today(go=False):
    lastId = 0
    from_time = get_today_str_start()
    to_time = get_today_str_end()
    sql="select logId,userId,url,creationTime,query,sessionEnd from  `search_query_log` where userid!=0 and query!='' and creationTime>'"+from_time+"' and creationTime< '"+to_time+"' order by logid asc;"
    print sql
    results = DataUtil.db_query('online','mydb',sql)
    if results!=None:
        for r in results:        
            __logId = r[0]
    return lastId
def start(mode):
    print 'start job in '+mode+' mode'
    if mode=="running_day":
        while True:
            job_process_today()
            print 'sleeping..'
            time.sleep(60)
    elif mode=="running_break_point":
        while True:
            job_process_break_point()
            print 'sleeping..'
            time.sleep(60)
    elif mode=="crontab_day":
        job_process_today()
    elif mode=="crontab_break_point":
        job_process_break_point()
def run_param():
    from_time='2016-02-14 00:00:00'
    to_time='2016-02-15 23:00:00'
    limit=100
    topn=10
    if(len(sys.argv)==1):
        log_job(from_time,to_time,limit)
    elif len(sys.argv)==4:
        log_job(sys.argv[1],sys.argv[2],sys.argv[3])
    else:
        print 'params error,usage:irrprecesion from_time to_time limit'
        exit(1)
if __name__ == '__main__':
    #start('running_day')
    #start('running_break_point')
    #start('crontab_day')
    #start('crontab_break_point')

    today = get_today_str()
    print 'runs success at '+today
    alert_title="job_tpl"
    alert('irdev','job_tpl','crontab run success',alert_title,'normal','open',True)
