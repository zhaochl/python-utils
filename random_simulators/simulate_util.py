#!/usr/bin/env python
# coding=utf-8
from random import *
def random_chinese_str():
    isOver = False
    _result=None
    while not isOver or _result==None:
        try:
            head = randint(0xB0, 0xCF)
            body = randint(0xA, 0xF)
            tail = randint(0, 0xF)
            val = ( head << 8 ) | (body << 4) | tail
            str = "%x" % val
            _result = str.decode('hex').decode('gb2312')  
            isOver=True
            break
        except:
            isOver=False
    return _result

if __name__=='__main__':
    print 'main'
    t=random_chinese_str()
    print t
