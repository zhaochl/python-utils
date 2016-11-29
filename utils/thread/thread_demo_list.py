#!/usr/bin/env python
# coding=utf-8
import threading 
from time import sleep, ctime 
import threading 
from time import sleep, ctime 
  
  
def thread_run(thread_id, thread_data): 
    print 'thread_id', thread_id, 'data:',thread_data,'at:', ctime() 
    sleep(thread_data) 
    print 'thread_id', thread_id, 'done at:', ctime() 
    
def main(): 
    print '---starting at:', ctime() 
    threads = [] 
    thread_data = [ 5,1 ] 
    nthread_data = range(len(thread_data)) 

    for i in nthread_data: 
        print 'i:',i
        t = threading.Thread(target=thread_run,args=(i, thread_data[i])) 
        threads.append(t) 

    for i in nthread_data:      # start threads 
        threads[i].start() 

    for i in nthread_data:      # wait for all 
        threads[i].join()    # threads to finish 

    print '---all DONE at:', ctime() 
  
if __name__ == '__main__': 
    main() 
