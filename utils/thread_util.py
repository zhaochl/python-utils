#!/usr/bin/env python
# coding=utf-8
import threading 
from time import sleep, ctime 
"""
class defined
"""
class ThreadUtil(threading.Thread): 
    def __init__(self, func, args, name=''): 
        threading.Thread.__init__(self) 
        self.name = name 
        self.func = func 
        self.args = args 
    
    def getResult(self): 
        return self.res 
    
    def run(self): 
        #print 'starting', self.name, 'at:', ctime() 
        self.res = apply(self.func, self.args) 
        #print self.name,'result:',self.res, 'finished at:', ctime() 
"""
thread run to process
"""
def thread_process(thread_id, data): 
    print '[start] thread_id', thread_id,',data',data, ' at:', ctime() 
    #sleep(data) 
    print '[done]thread_id', thread_id, ' at:', ctime() 
    return data
"""
every job one thread
"""
def job_all_thread_mode(): 
    jobs = [ 4, 2 ] 
    print 'starting at:', ctime() 
    threads = [] 
    njobs = range(len(jobs)) 
    
    for i in njobs: 
        t = ThreadUtil(thread_process, (i, jobs[i]), thread_process.__name__) 
        threads.append(t) 
    
    for i in njobs: 
        threads[i].setDaemon(False) 
        threads[i].start() 
    
    for i in njobs: 
        threads[i].join() 
    
    print 'all DONE at:', ctime() 
    for i in njobs: 
        r = threads[i].getResult()
        print 'results:',r
"""
limit thread count to assign the jobs
"""
def job_limit_thread_mode():
    jobs_all=[11,22,33,44,55,66]
    thread_pool = [] 
    thread_len = 2
    thread_range = range(thread_len)
    for index,job in enumerate(jobs_all):
        #print index,job 
        #print '---------len(thread_pool):',len(thread_pool)
        if len(thread_pool)<thread_len:
            #print 'new thread'
            t = ThreadUtil(thread_process, (index, job), thread_process.__name__) 
            thread_pool.append(t)
        else: 
            print 'thread run start'
            for i in thread_range: 
                thread_pool[i].setDaemon(False) 
                thread_pool[i].start() 
    
            for i in thread_range: 
                thread_pool[i].join() 
    
            print 'all DONE at:', ctime() 
            for i in thread_range: 
                r = thread_pool[i].getResult()
                print 'results:',r
            
            print 'thread run end'
            thread_pool = [] 
            
if __name__ == '__main__': 
    job_all_thread_mode()
    #job_limit_thread_mode()
