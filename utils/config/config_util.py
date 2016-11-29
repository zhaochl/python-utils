#!/usr/bin/env python
# coding=utf-8
import ConfigParser
import time
import os
config = ConfigParser.RawConfigParser()
global __setting
__setting = {}
def set_config(key,val):
    global __setting
    __setting[key] =val
def get_config(key):
    global __setting
    __result = None
    if __setting. has_key(key):
        __result = __setting[key]
    return __result

def write_config(section_name,config_dict,file="default.conf"):
    config.add_section(section_name)#增加section
    for key,val in config_dict.iteritems():
        config.set(section_name, key, val)#增加option
    fp = open(file, "w")
    config.write(fp)
def read_config(section_name,config_key,file="default.conf"):
    config.read(file)
    #print config.sections()
    _result=None
    _result = config.get(section_name,config_key)
    return _result

"""
[{'conf1':{'section1':{'k1':'v1'},'section2':{'k1':'v2'}}},{'conf2':{'s1':{'k1':'v1'}}}]
"""
def load_confs():
    results=[]
    
    conf_files = []
    try:
        #conf_dir ='../conf.d/'
        conf_dir ='.'
        for root,dirs,files in os.walk(conf_dir):
            for f in files:
                p =os.path.join(root,f)
                if '.conf' in f:
                    conf_files.append(p)
    except:
        print 'load_confs error,exit'
        exit(1)
    print conf_files
    if len(conf_files) >0:
        for _f in conf_files:
            config.read(_f)
            sections = config.sections()
            _f_name = _f.strip('./')
            #if sections!=None:
            #    print _f,_f_name, sections
            for sec in sections:
                sec_key_list = config.options(sec)
                for sec_key in sec_key_list:
                    sec_val = config.get(sec,sec_key)
                    print sec_val
    
def t1():
    print '--config--util'
    set_config('a',1)
    a = get_config('a')
    print a
    task = {}
    task["key1"] = 'val1'
    task["key2"] = 'val2'
    
    write_config('demo_section',task)
    a= read_config('demo_section','key1')
    print a
if __name__=='__main__':
    t = config.read("default.conf")
    print  t
    print config.get('sec_a','a_key1')
    print config.get('sec_a','a_key11111')
    print '--------'
    t = config.sections()
    print t
    
    opts = config.options("sec_a") 
    print 'options:', opts 
    
    kvs = config.items("sec_a") 
    print 'sec_a:', kvs 
    
    t= load_confs()
    print t
