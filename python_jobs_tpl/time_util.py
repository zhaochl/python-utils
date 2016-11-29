#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
class TimeUtil:
    __start=0
    __end=0
    __cost=0
    @staticmethod
    def __init__(self,start,end):
        self.__start = start
        self.__end = end
        self.__cost = end-start
    @staticmethod
    def start():
        TimeUtil.__start = time.time()
        #print 'TimeUtil start.',TimeUtil.__start
        print 'TimeUtil.start.',TimeUtil.__start

    @staticmethod
    def stop():
        TimeUtil.__end = time.time()
        TimeUtil.__cost = TimeUtil.__end - TimeUtil.__start
        print 'TimeUtil.cost:',TimeUtil.__cost,'ms'

    @staticmethod
    def cost():
        TimeUtil.__cost = TimeUtil.__start - TimeUtil.__end
        return TimeUtil.__cost

if __name__=='__main__':
    TimeUtil.start()
    print __file__
    print __name__
    print 'demo main.'
    TimeUtil.stop()
    print TimeUtil.cost()
