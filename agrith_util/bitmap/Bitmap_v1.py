#!/usr/bin/env python
#coding: utf8


#http://my.oschina.net/goal/blog/200347

class Bitmap(object):
    def __init__(self, max):
        self.size = int((max + 31 - 1) / 31) #向上取整

'''
首先需要初始化bitmap。拿90这个整数来说，因为单个整型只能使用31位，所以90除以31并向上取整则可得知需要几个数组元素
'''
if __name__ == '__main__':
    bitmap = Bitmap(90)
    print "需要 %d 个元素。" % bitmap.size
