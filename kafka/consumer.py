#!/usr/bin/env python
# coding=utf-8
#pip install kafka-python
from kafka import KafkaConsumer
print 'start.'
#topic_id='cf-api1_cf_biz'
topic_id='foobar'
consumer = KafkaConsumer(topic_id,bootstrap_servers="bi-dn12:9092,bi-dn13:9092,bi-dn14:9092",auto_offset_reset='earliest')
print 'connnect.'
for msg in consumer:
    print (msg)
print 'ok'
