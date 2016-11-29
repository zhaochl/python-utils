#!/usr/bin/env python
# coding=utf-8
import thread
import time
mylock = thread.allocate_lock()  #Allocate a lock
num=0  #Shared resource

def add_num(name):
    print 'add_num'
    global num
    while True:
        mylock.acquire() #Get the lock 
        # Do something to the shared resource
        print 'Thread %s locked! num=%s'%(name,str(num))
        if num >= 5:
            print 'Thread %s released! num=%s'%(name,str(num))
            mylock.release()
            thread.exit_thread()
        num+=1
        print 'Thread %s released! num=%s'%(name,str(num))
        mylock.release()  #Release the lock.

def test():
    thread.start_new_thread(add_num, ('A',))
    thread.start_new_thread(add_num, ('B',))

if __name__== '__main__':
    test()
    while True:
        if num >=5:
            print 'sub thread add over will exit.'
            break
        print 'sleeping...num:',num
        time.sleep(1)
        





