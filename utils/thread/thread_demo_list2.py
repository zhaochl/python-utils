#!/usr/bin/env python
# coding=utf-8
import threading 
from time import sleep, ctime 
  
#t = threading.Thread(target=ThreadFunc(loop, (i, loops[i]), loop.__name__)) 
#t = ThreadFunc(loop, (i, loops[i]), loop.__name__)
class ThreadFunc(object):
    def __init__(self, func, args, name=''): 
        self.name = name 
        self.func = func 
        self.args = args 
  
    def __call__(self): 
        apply(self.func, self.args)
        print self.name+' is called' 
  
def loop(nloop, nsec): 
    print 'start loop', nloop, 'at:', ctime() 
    sleep(nsec) 
    print 'loop', nloop, 'done at:', ctime() 
  
def main(): 
    loops = [ 4, 2 ]
    print 'starting at:', ctime() 
    threads = [] 
    nloops = range(len(loops)) 
    
    for i in nloops:  # create all threads 
        tfun = ThreadFunc(loop, (i, loops[i]), loop.__name__)
        t = threading.Thread(target=tfun) 
        threads.append(t) 
    
    for i in nloops:  # start all threads 
        threads[i].start() 
    
    for i in nloops:  # wait for completion 
        threads[i].join() 
    
    print 'all DONE at:', ctime() 
  
if __name__ == '__main__': 
    main() 
