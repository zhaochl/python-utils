#!/usr/bin/python
# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch
from data_util import *
import time
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def import_investor__log_to_es():
    print '--import log to es---'
    es = Elasticsearch("localhost")
    offset_file = '.import_market_offset'
    offset_old = get_offset(offset_file)
    #select l.logId,l.userId,u.name,l.objectId,p.title,l.type,l.localTime,unix_timestamp(l.localTime) from `investor_app_log` l,`user` u,`project` p
    log_results = DataUtil.get_applogs_cf_from_logid(offset_old,100)
    lastLogId=0
    if log_results:
        for r in log_results:
            logId = r[0]
            userId = r[1]
            userName=r[2].strip().encode('utf8','ignore')
            projectId=r[3]
            projectName=r[4].strip().encode('utf8','ignore')
            type=r[5].strip().encode('utf8','ignore')
            #localTime=r[6].strip().encode('utf8','ignore')
            localTime=r[6]
            timestamp=r[7]
            #print logId,userName,projectName,type
            en_doc={}
            en_doc['logId'] = logId
            en_doc['userId'] = userId
            en_doc['userName'] = userName
            en_doc['projectName'] =projectName
            en_doc['type'] = type
            en_doc['localTime'] = localTime
            en_doc['timestamp'] =timestamp
            utc_t = datetime.datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
            en_doc['@timestamp']=utc_t
            #print en_doc
            res = es.index(index="idx_investor_app_log", doc_type='investor_app_log', body=en_doc)
            #print res
            lastLogId=logId
    set_offset(offset_file,lastLogId)
def get_offset(offset_file):
    offset=0
    try:
        with open(offset_file) as f:
            offset = int(f.readline())
    except Exception, e:
        offset = 0
    return offset
def set_offset(offset_file,offset):
    with open(offset_file, 'w') as f:
        f.write('{0}\n'.format(offset))

if __name__=='__main__':
    print 'import investor_app_log to es start.'
    IMPORT_TYPE = 'day'  # all,delta,day
    
    offset_file = '.import_market_offset'
    #offset=1
    #set_offset(offset_file,offset)

    while True:
        offset2 = get_offset(offset_file)
        print 'offset:',offset2
        import_investor__log_to_es()
        time.sleep(3)
        #if offset2>2000000:
        #    print 'import success.'
        #    break
