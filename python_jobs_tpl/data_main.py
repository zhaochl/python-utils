#!/usr/bin/env python
# coding=utf-8
from data_util import *
from date_util import *
from pdb import *
def query_news_spider_z(from_time,to_time,time_gap):
    # url must before title at 4.20
    sql="SELECT `aid` ,`url` ,`title`,`fromsite`,`category_name`,`pubtime` ,`addtime`,`pagetype` FROM `doc_tab_z` where `addtime` >'"+from_time+"' and `addtime` <'"+to_time+"' ORDER BY `aid` DESC limit 10000;"
    print sql 
    return convert_results_server('irweb','news_leads',sql)
def check_exist_key(key):
    exist = False
    sql="select name,value from rec_params where name='"+key+"'"
    print sql
    results = DataUtil.db_query('irweb','mydb',sql)
    if results==None or len(results)==0:
        exist = False
    else:
        exist = True
    return exist
def add_or_update_rec_params(key,value):
    #set_trace()
    sql=""
    if check_exist_key(key):
        print 'exist,update'
        sql = "update rec_params set value='"+value +"' where name='"+key+"'"
    else:
        print 'not exist,add'
        sql ="insert into rec_params (name,value) values ('"+key+"','"+value+"')"
    print sql
    DataUtil.db_update('irweb','mydb',sql)
    return sql
def convert_results(sql):
    results,colum = DataUtil.db_query_info('online','mydb',sql)
    colum_len = len(colum)
    print colum_len
    results_data =[]
    if results!=None:
        for r in results:
            obj ={}
            for i in range(colum_len):
                colum_name = colum[i]
                tmp_row =  r[i]
                obj[colum_name] = str(tmp_row)
            results_data.append(obj)
    #print results_data
    #print colum
    return colum,results_data,sql


if __name__=='__main__':
    print '-data_main-'
    from_time = '2016-03-27 00:00:00'
    to_time = '2016-03-27 23:59:59'
    time_gap = 1
    #stat_tab(from_time,to_time,time_gap)
    r,c,s = stat_type(from_time,to_time,time_gap)
