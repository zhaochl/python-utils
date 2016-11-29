#!/usr/bin/env python
# coding=utf-8
from data_util import *
from date_util import *
from cache_util import *
from pdb import *
import logging
import os
from datetime import datetime

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    #datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(os.getcwd(),'_log_loader.log'),
                    filemode='a')
def p(info):
    _n= datetime.now()
    _today= _n.strftime("%Y-%m-%d %H:%M:%S")
    print _today+" "+info
def I(info):
    logging.info(info)
    p(info)

def _load_log_tpl():
    I('load_investor_app_log start.')
    
    lastId=0
    limit = 10000
    results =None
    while True:
        sql="""
        select userId,objectId,
        type,subtype,
        duration,creationTime,logId 
        from investor_app_log 
        where
        logId>{0}
        order by logId asc limit {1};
        """.format(str(lastId),limit)
        
        
        results = DataUtil.db_query('online','mydb',sql)
        
        if len(results)==0:
            I('load_investor_app_log end.')
            break
        else:
            for r in results:
                userid=int(r[0])
                projectId=int(r[1])
                type =r[2].decode('utf8','ignore')
                subtype =r[3].decode('utf8','ignore')
                duration = r[4]
                creationtime = str(r[5])
                logId=int(r[6])
                lastId=logId
                
                past_week = calc_past_week(creationtime)
                #print 'past_week:'+str(past_week)
                # 如果日期时间大于一年，或者间隔小于设定阈值
                if past_week>52 or duration <sim_project_ducation:
                    continue
                sim_project_weight_tmp = 0.0
                exp_str = "logId:"+str(logId)+\
                        "#userid:"+str(userid)+\
                        "#projectId:<em>"+str(projectId)+"</em>"+\
                        "#type:"+str(type)+\
                        "#subtype:"+str(subtype)+\
                        "#duration:"+str(duration)+\
                        "#creationtime:"+creationtime+\
                        "#past_week:"+str(past_week)+\
                        "#weight:"+str(sim_project_weight_tmp)
                
                if type=='PROJECT_BP':
                    sim_project_weight_tmp = sim_project_weight_bp_arr[past_week]
                elif type=='COLLECT_PROJECT':
                    sim_project_weight_tmp = sim_project_weight_collect_arr[past_week]
            #//for-results
        I('batch end,lastId:'+str(lastId))
    #//while true
    I('load_investor_app_log ok.lastId:'+str(lastId))
   
if __name__=='__main__':
    print 'main'
    #init_all_project_user_score_cache()
    load_investor_app_log()
