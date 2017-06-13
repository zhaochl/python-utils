#!/usr/bin/env python
# coding=utf-8
import commands
import sys
from docopt import docopt
#from handler import LogFileClient
from sdutil.log_util import getLogger
from sdutil.date_util import *
reload(sys)
sys.setdefaultencoding('utf-8')
from elasticsearch import Elasticsearch

from pdb import *
import requests
import json

logger = getLogger(__name__, __file__)
"""
host like:"http://172.17.0.33:8081"
"""
def count_from_es(host,index,query_str,startTime,endTime,scroll=False):
    logger.info('search_from_es startTime:%s,endTime:%s'%(startTime,endTime))
    startTimeStamp = int(str2timestamp(startTime))*1000
    endTimeStamp = int(str2timestamp(endTime))*1000+999
    data_post_search = {"query":{"filtered":{"query":{"query_string":{"query":query_str,"analyze_wildcard":'true'}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":startTimeStamp,"lte":endTimeStamp,"format":"epoch_millis"}}}],"must_not":[]}}}}}
    logger.info('search_from_es,post_data:%s'%(data_post_search))
    es = Elasticsearch(host,timeout=120)

    response = es.count(index=index, body=data_post_search)
    return response

def do_search(host,index,query_str,startTimeStamp,endTimeStamp,scroll,_source,time_step):
    es = Elasticsearch(host,timeout=120)
    response ={}
    data_post_search = {"query":{"filtered":{"query":{"query_string":{"query":query_str,"analyze_wildcard":'true'}},"filter":{"bool":{"must":[{"range":{"@timestamp":{"gte":startTimeStamp,"lte":endTimeStamp,"format":"epoch_millis"}}}],"must_not":[]}}}}}
    logger.info('search_from_es,post_data:%s'%(data_post_search))
    if not scroll:
        
        if _source:
            response = es.search(index=index, body=data_post_search,size=10000,_source=_source)
        else:
            response = es.search(index=index, body=data_post_search,size=10000)
    else:
        page_size=10000
        scan_resp =None
        if _source:
            scan_resp = es.search(index=index, body=data_post_search,search_type="scan", scroll="5m",size=page_size,_source=_source)
        else:
            scan_resp = es.search(index=index, body=data_post_search,search_type="scan", scroll="5m",size=page_size)

        scrollId= scan_resp['_scroll_id']
        response={}
        total = scan_resp['hits']['total']
        response_list =[]
        scrollId_list =[]
        for page_num in range(total/page_size + 1):
            response_tmp ={}
            response_tmp = es.scroll(scroll_id=scrollId, scroll= "5m")
            #es.clear_scroll([scrollId])
            scrollId = response_tmp['_scroll_id']
            scrollId_list.append(str(scrollId))
            response_list.append(response_tmp)
            if response.has_key('hits'):
                _hits = response['hits']
                _hits['hits']+=response_tmp['hits']['hits']
                response['hits'] = _hits
            else:
                response['hits'] = response_tmp['hits']

    return response
def search_from_es(host,index,query_str,startTime,endTime,scroll=False,_source=None,time_step=0):
    logger.info('search_from_es startTime:%s,endTime:%s'%(startTime,endTime))
    startTimeStamp = int(str2timestamp(startTime))*1000
    endTimeStamp = int(str2timestamp(endTime))*1000+999
    
    all_response={}
    timegap = endTimeStamp-startTimeStamp
    
    if time_step>0:
        _s1=startTimeStamp
        _s2=startTimeStamp+time_step
        run_time =0
        all_response = {}
        time_count = {}
        while(_s2<=endTimeStamp):
            response_tmp = do_search(host,index,query_str,_s1,_s2,scroll,_source,time_step)
            #response_tmp = do_search(_s1,_s2)
            if all_response.has_key('hits'):
                _hits = all_response['hits']
                _hits['hits']+=response_tmp['hits']['hits']
                all_response['hits'] = _hits
            else:
                all_response['hits'] = response_tmp['hits']
            run_time+=1
            _s1=_s1+time_step
            _s2 = _s2+time_step
            
            if time_count.has_key(_s1):
                time_count[_s1]+=1
            else:
                time_count[_s1]=1
            
            if time_count.has_key(_s2):
                time_count[_s2]+=1
            else:
                time_count[_s2]=1
            
            print '----run_time:',run_time,'_s1:',_s1,',_s2:',_s2,',len:',len(all_response['hits']['hits'])
            print '-s1--',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(_s1/1000))
            print '-s2--',time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(_s2/1000))
            print time_count
            time.sleep(2)
    else:
        all_response = do_search(host,index,query_str,startTimeStamp,endTimeStamp,scroll,_source,time_step)
    
    return all_response
               
