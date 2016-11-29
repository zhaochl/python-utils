#!/usr/bin/env python
# coding=utf-8
import ConfigParser 
import time  
config = ConfigParser.RawConfigParser() 
  
def write_config():
    task = {}
    task["id"] = 1
    task["package"] = "exe"
    task["timeout"] = 150
    task["dst_filename"] = "1.exe"
    task["custom"] = "" 
    task["test_list"] = "['a','b','c']"
    task["test_dict"] = "{'a':1}" 
    config.add_section("analysis")#增加section 
    config.set("analysis", "id", task["id"])#增加option 
    config.set("analysis", "target", task["dst_filename"]) 
    config.set("analysis", "package", task["package"]) 
    config.set("analysis", "timeout", task["timeout"]) 
    config.set("analysis", "test_list", task["test_list"]) 
    config.set("analysis", "test_dict", task["test_dict"]) 
    config.set("analysis", "started", time.asctime()) 
    fp = open("analy.conf", "w") 
    config.write(fp)
def read_config():
    config.read("analy.conf") 
    if config.has_option("analysis", "timeout"): 
        print config.get("analysis", "timeout")       
        print config.sections() 
        print config.get("analysis", "package") 
        print config.getint("analysis", "id") 
        l = config.get("analysis", "test_list") 
        print ' print -config list'
        if l!=None:
            l = list(l)
            for _l in l:
                print _l
        print ' print -config dict'
        d= config.get("analysis", "test_dict")
        d=dict(d)
        if d!=None:
            for k,v in d.iteritems():
                print k,v
if __name__=='__main__':
    print '--config--util'
    write_config()
    read_config()
