#!/usr/bin/env python
# coding=utf-8
from data_util import *
from date_util import *

"""
return :
['searchtype', 'creationTime']
[{'creationTime': '2016-03-27 00:20:17'}]
"""
def stat_tab(from_time,to_time,time_gap):
    sql = "SELECT searchtype,count(1) as count FROM search_query_log where `creationTime` > '"+from_time+"' and `creationTime`<'"+to_time+"' and searchtype!='' GROUP BY searchtype limit 10;"
    #sql="SELECT searchtype,creationTime as count FROM search_query_log where `creationTime` > '2016-03-27 00:00:00' and `creationTime`<'2016-03-27 23:59:59' and searchtype!='';"
    results,colum = DataUtil.db_query_info('online','mydb',sql)
    colum_len = len(colum)
    results_data =[]
    print colum
    if results!=None:
        for r in results:
            #searchtype = r[0].encode('utf8')
            #creationTime = r[1]
            #count = r[2]
            #print r
            obj ={}
            for i in range(colum_len):
                colum_name = colum[i]
                tmp_row =  r[i]
                obj[colum_name] = str(tmp_row)
            results_data.append(obj)
    print results_data
    return colum,results_data,sql
"""
sql="SELECT searchtype,creationTime FROM search_query_log where `creationTime` > '2016-03-27 00:00:00' and `creationTime`<'2016-03-27 23:59:59' and searchtype!='';"
return :
['searchtype', 'creationTime']
[{'creationTime': '2016-03-27 00:20:17'}]
"""
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
def stat_type(from_time,to_time,time_gap):
    sql="SELECT type,count(1)  as count FROM `mydb`.`search_query_log` where `creationTime` > '"+from_time+"' and `creationTime`<'"+to_time+"' and url is not null and url != '' group by type;"
    return convert_results(sql)

def stat_click_users(from_time,to_time,time_gap):
    sql="SELECT count(DISTINCT( `userId` )) FROM `mydb`.`search_query_log` where `creationTime` > '"+from_time+"' and `creationTime`<'"+to_time+"' and url is not null and url != '' ;"
    
    return convert_results(sql)
def stat_topn_query(from_time,to_time,time_gap):
    sql="SELECT query,count(1) as c FROM `search_query_log` where query!='' and `creationTime` > '"+from_time+"' and `creationTime`<'"+to_time+"' group by query order by c desc limit 20;"
    return convert_results(sql)

def stat_max_query_users(from_time,to_time,time_gap):
    sql="""
    select name,count(1) as c from (
    SELECT q.*,u.`userName`,u.name FROM `mydb`.`search_query_log` as q left join user as u on q.userid=u.userid where q.`creationTime` > '{0}' and q.`creationTime` <'{1}' and url != ''
    ) as t1
    group by name order by c desc limit 50;
    """.format(from_time,to_time)
    return convert_results(sql)
if __name__=='__main__':
    print '-data_main-'
    from_time = '2016-03-27 00:00:00'
    to_time = '2016-03-27 23:59:59'
    time_gap = 1
    #stat_tab(from_time,to_time,time_gap)
    r,c,s = stat_type(from_time,to_time,time_gap)
