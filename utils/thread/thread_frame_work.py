#!/usr/bin/env python
# coding=utf-8
import threading 
from time import sleep, ctime 
  
  
class MyThread(threading.Thread): 
    def __init__(self, func, args, name=''): 
        threading.Thread.__init__(self) 
        self.name = name 
        self.func = func 
        self.args = args 
    
    def getResult(self): 
        return self.res 
    
    def run(self): 
        print 'starting', self.name, 'at:', ctime() 
        self.res = apply(self.func, self.args) 
        print self.name,'result:',self.res, 'finished at:', ctime() 

def loop(nloop, nsec): 
    print 'start loop', nloop, 'at:', ctime() 
    sleep(nsec) 
    print 'loop', nloop, 'done at:', ctime() 
    return nsec

def main(): 
    loops = [ 4, 2 ] 
    print 'starting at:', ctime() 
    threads = [] 
    nloops = range(len(loops)) 
    
    for i in nloops: 
        t = MyThread(loop, (i, loops[i]), 
        loop.__name__) 
        threads.append(t) 
    
    for i in nloops: 
        threads[i].setDaemon(False) 
        threads[i].start() 
    
    for i in nloops: 
        threads[i].join() 
    
    print 'all DONE at:', ctime() 
    for i in nloops: 
        r = threads[i].getResult()
        print 'results:',r
      
if __name__ == '__main__': 
    main()
