#!/usr/bin/env python
# coding=utf-8
from comm_util import *
class User:
    name = ''
    age = 0
    course = {}

    def __init__(self,namex,agex,coursex=None):
        self.name=namex
        self.age=agex
        self.course = coursex

    def getName(self):
        return self.name
    def getAge(self):
        return self.age

if __name__ == '__main__':
    c = {'math':10}
    p = User('zhangsan',1)
    print p.name
    print p.getName()
    setattr(p,'age',100)
    print p.getAge()
    print getattr(p,'t','no t attr')
    userList =[]
    p1 = User('zhangsan1',1)
    userList.append(p1)
    p2 = User('zhangsan2',2)
    userList.append(p2)
    p3 = User('zhangsan3',3)
    userList.append(p3)
    p4 = User('zhangsan4',4,c)
    userList.append(p4)
    
    for u in userList:
        print u.name,u.age,u.course

    


