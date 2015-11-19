#!/usr/bin/env python
#coding=utf-8
import time
import json
import sys,redis
reload(sys)
sys.setdefaultencoding('utf8')

def conn_redis():
	r = redis.StrictRedis(host='127.0.0.1', port=6379)
	return r
def import_data():
	date=time.strftime('%Y-%m-%d',time.localtime(time.time()))
	file_name='data.json/data_export_'+date+'.json'
	print file_name
	r = conn_redis()
	fp=open(file_name,'r')
	#read_data = fp.read()
	#print read_data
	data = json.loads(fp.read())
	#print data
	data=r.set('list:logstash_www1',data)
	fp.close()
	date_log= time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
	print 'info:'+date_log+':'+'import from file '+file_name+' success,then add to redis success.'
import_data()