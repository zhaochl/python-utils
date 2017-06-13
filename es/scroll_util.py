#!/usr/bin/env python
# coding=utf-8

import sys
from datetime import *
import time
from elasticsearch import Elasticsearch

CONST_ES_HOST="http://172.17.0.1:8081"
CONST_TABLE='export_table'
CONST_INDEX='stat-*'

def str2timestamp(str1,formatStr='%Y-%m-%d %H:%M:%S'):
    _t = time.mktime(time.strptime(str1,formatStr))
    return int(_t)



def search_from_es(host,index,query_str,startTime,endTime,scroll=True):
    print('search_from_es startTime:%s,endTime:%s'%(startTime,endTime))
    startTimeStamp = int(str2timestamp(startTime))*1000
    endTimeStamp = int(str2timestamp(endTime))*1000+999
    data_post_search = {"query":{"filtered":{"query":{"query_string":{"query":query_str,"analyze_wildcard":'true'}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":startTimeStamp,"lte":endTimeStamp,"format":"epoch_millis"}}}],"must_not":[]}}}}}
    print('search_from_es,post_data:%s'%(data_post_search))
    es = Elasticsearch(host)
    response={}
    if not scroll:
        response = es.search(index=index, body=data_post_search,size=10000)
    else:
        page_size=10000
        scan_resp = es.search(index=index, body=data_post_search,search_type="scan", scroll="1m",size=page_size,_source=['op','time'])
        scrollId= scan_resp['_scroll_id']
        response={}
        total = scan_resp['hits']['total']
        response_list =[]
        for page_num in range(total/page_size + 1):
            print 'scroll page_num:',page_num
            response_tmp ={}
            response_tmp = es.scroll(scroll_id=scrollId, scroll= "1m")
            scrollId = response_tmp['_scroll_id']
            response_list.append(response_tmp)
            if response.has_key('hits'):
                _hits = response['hits']
                _hits['hits']+=response_tmp['hits']['hits']
                response['hits'] = _hits
            else:
                response['hits'] = response_tmp['hits']
    return response

def fetch_es(startTime,endTime,scroll=True,condition='all'):
    host = CONST_ES_HOST
    index = CONST_INDEX
    query_str='*'
    if condition!='all':
        query_str="op:case_submit_patient_info OR op:case_submit_payee_info OR op:case_submit_treatment_info OR op:case_finish OR op:case_draw_cash_apply OR op:case_submit_for_review OR op:share"
    res = search_from_es(host,index,query_str,startTime,endTime,scroll=scroll)
    return res

if __name__=='__main__':

    startTime='2017-04-13 16:00:00'
    endTime='2017-04-13 17:00:00'
    print '---scroll True--'
    res = fetch_es(startTime,endTime,scroll=True)
    total = res['hits']['total']
    count = len(res['hits']['hits'])
    #print  198704 198704
    print total,count
    print '---scroll False--'
    res = fetch_es(startTime,endTime,scroll=False)
    total = res['hits']['total']
    count = len(res['hits']['hits'])
    #print 198704 198704
    print total,count
    
