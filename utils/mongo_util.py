#!/usr/bin/env python
# coding=utf-8
import pymongo

def init_mongo(dbname):
    client = pymongo.MongoClient("localhost", 27017)
    db = client.dbname


if __name__=='__main__':
    client = pymongo.MongoClient("localhost", 27017)
    db = client.monitoring
    dbname = db.name
    print dbname
    collect_alerts = db.alerts
    print collect_alerts

    
    l = db.alerts.find_one()
    print l

