#!/usr/bin/env python
# coding=utf-8
#pip install kafka-python

from kafka import KafkaProducer
print 'start..'
producer = KafkaProducer(bootstrap_servers='bi-dn12:9092,bi-dn13:9092,bi-dn14:9092')
for _ in range(100):
    producer.send('foobar', b'some_message_bytes')
print 'success'
