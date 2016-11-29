#!/usr/bin/python
# -*- coding: utf-8 -*-
from peewee import *
import time
db = MySQLDatabase(host = 'irweb', user = 'root', passwd = 'root', database = 'mydb')
#print db

class Less3(Model):
    class Meta:
        db_table = 'search_less3_exception_log'
        database = db
    log_id = PrimaryKeyField()
    project_id = IntegerField()
    title = CharField()
    tag = CharField()
    weight = CharField()
    create_time = IntegerField()
    update_time = IntegerField()
    status = IntegerField()

def addLess3(project_id,title,tag,weight):
    print '--addLess3--start--'
    create_time = (int)(time.time())
    #User(username='admin',password='admin',sex=1,gid=1)
    less3 = Less3(project_id=project_id,title=title,tag=tag,weight=weight,create_time=create_time,update_time=create_time,status=0)
    less3.save()
    print '--addLess3--end--'

def findLess3(project_id):
    result= object
    try:
        ul = Less3.select().where(Less3.project_id == project_id).get()
        result=ul
    except:
        result=None
    return result

def updateLess3(project_id,key,value):
    result= object
    #print '---update start---'
    try:
        ul = Less3.select().where(Less3.project_id == project_id).get()
        if ul:
            #print 'find success'
            if key=='title':
                ul.title = value
            elif key=='tag':
                ul.tag = value
            elif key=='weight':
                ul.weight =value
            elif key=='update_time':
                ul.update_time=value
            else:
                raise 'unkown field:'+key
            ul.save()
    except:
        result=None
    #print '---update start---'

def findAllLess3():
#     print '---find all start---'
    result= object
    try:
        ulist = Less3.select()
        result=ulist
    except:
        result=None
#     print '---find all end---'
    return result

def print_Less3(less):
    print '---print Less start---'
    print 'log_id:'+str(less.log_id)+',project_id:'+str(less.project_id)+',title:'+less.title+',tag:'+less.tag+',create_time:'+str(less.create_time)
    print '---print Less3 start---'
#addLess3('22', 'test', 'tag1', '11')
