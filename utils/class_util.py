#!/usr/bin/env python
# coding=utf-8
class Message:
    def __init__(self,msg):
        self.msg = msg
    def print_msg(self):
        print self.msg
class a:
    def __init__(self,_a,_b):
        self.a = _a
        self.b = _b


if __name__=='__main__':
    m = Message('hello')
    m.print_msg()
    a1 = a(1,2)
    print a1,a1.__dict__
