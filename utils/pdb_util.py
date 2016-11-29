#!/usr/bin/env python
# coding=utf-8
from pdb import *

"""
http://www.cnblogs.com/dkblog/archive/2010/12/07/1980682.html
进入pdb 命令行模式
h 帮助
l 查看当前代码快
b 11 在11行设置断点
cl 消除所有断点
p a 输出a变量值
n(ext)，让程序运行下一行，如果当前语句有一个函数调用，用n是不会进入被调用的函数体中的 
s(tep)，跟n相似，但是如果当前有一个函数调用，那么s会进入被调用的函数体中 
c(ont(inue))，让程序正常运行，直到遇到断点 
j(ump)，让程序跳转到指定的行数 
(Pdb) j 497
"""
if __name__ =='__main__':
    print '--pdf--util-'
    a=1
    b=2
    c=a+b
    set_trace()
    print c


