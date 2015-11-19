#!/usr/bin/env python
#coding=utf-8
import time
import json
import sys,redis
reload(sys)
sys.setdefaultencoding('utf8')

def conn_redis():
        r = redis.StrictRedis(host='127.0.0.1', port=6379)
        #data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]

        #r.set('foo',json.dumps(data))
        #a=r.get('foo')
        #print a
        return r
def export_data():
        date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        file_name='data.json/data_export_'+date+'.json'
        f=file(file_name,'w+')
        r = conn_redis()
	#print r
        #data=r.lrange('list:logstash_www',0,-1)
        data=r.lrange('list:logstash_www',0,-1)
        json.dump(data, f)
        f.flush()
	date_log= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	print 'info:'+date_log+':'+'export to file '+file_name+' success,then clear redis success.'
	r.delete('list:logstash_www')
export_data()