#!/usr/bin/env python
# coding=utf-8
from data_util import *
from http_util import *
from sort_util import *
from redis_util import *
import time
from thread_util import *
from data_main import *
           
def url_search(projectId,title,day):
    host = 'localhost'
    host2 = 'localhost'
    #before_stamp = (int(time.time())-day*60*60*24)*1000
    before_stamp = int(time.time())-day*60*60*24
    before_stamp=str(before_stamp)
    _project_pub_count={}
    _project_pubtitle_count={}
    url ="http://"+host+"/search?query="+title+"&bejson=1&crs=1&pagesize=1&type=64&period="+before_stamp
    #url2 ="http://"+host2+"/search?query="+title+"&bejson=1&crs=1&pagesize=200&type=64&t=1457509108000&period="+before_stamp
    url_results = get_json_from_url(url)
    if url_results==None:
        return
    matchcount = url_results['matchcount']
    if matchcount>0:
        _project_pub_count[projectId] = str(matchcount).encode('utf8')
        _project_pubtitle_count[title] = str(matchcount).encode('utf8')
    if int(matchcount)> 0:
        set_hash_one('news_pub_matchcount:'+str(day),projectId,matchcount)
    #    print projectId,title,' count is ',matchcount,',url:',url2
    #return _project_pubtitle_count

    return _project_pub_count
def url_search_thread(day):
    project_info =None
    #{'title':projectId}
    _project_pub_count ={}
    project_info = get_project_info()
    print len(project_info)
    thread_pool = []
    thread_len = 5
    thread_range = range(thread_len)
    ii=0
    index = len(project_info)
    break_point = index
    break_point_key ="news_project_break_point_"+str(day)
    break_point_tmp = get_string(break_point_key)
    if break_point_tmp!=None:
        break_point = int(break_point_tmp)
    for _title,_projectId in project_info.iteritems():
        print 'index:',index
        index-=1
        if index>=break_point:
            print 'continue.'
            continue
        else:
            set_string(break_point_key,index)
        """
        ii+=1
        if ii>11:
            break
        """
        #print _title,_projectId
        if len(thread_pool)<thread_len:
            #print 'new thread'
            t = ThreadUtil(url_search, (_projectId, _title,day), url_search.__name__) 
            thread_pool.append(t)
        else: 
            #print 'thread run start'
            for i in thread_range: 
                thread_pool[i].setDaemon(False) 
                thread_pool[i].start() 
    
            for i in thread_range: 
                thread_pool[i].join() 
    
            #print 'all DONE at:', ctime() 
            for i in thread_range: 
                t_results = thread_pool[i].getResult()
                #print 'results:',t_results 
                if t_results!=None:
                    for tk,tv in t_results.iteritems():
                        _project_pub_count[tk] = tv
            #print 'thread run end'
            thread_pool = []
        #time.sleep(2)
    #//for   
    print '*'*50
    print 'get url end,will order,len:',len(_project_pub_count)
    sort_results = []
    sort_results = sort_dict(_project_pub_count,'v')
    topk=10 
    if len(sort_results)<topk:
        topk = len(sort_results)

    topk_result = sort_results[0:topk]
    print topk_result
    #print _project_pub_count
    print 'over'
if __name__=='__main__':
    t= get_project_info()
    print len(t)
    
    t= get_leads_info()
    print len(t)
    """
    days=[1,3,7]
    for day in days:
        print 'day,',day
        url_search_thread(day)
    """
    #title='云飞思'
    #projectId='18178'
    #t= url_search(projectId,title)
