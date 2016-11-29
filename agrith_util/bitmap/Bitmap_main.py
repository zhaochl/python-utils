#!/usr/bin/env python
#coding: utf8

from Bitmap_v2 import *
#import Bitmap_v2
if __name__ == '__main__':
    MAX = 879
    suffle_array = [45, 2, 78, 35, 67, 90, 879, 0, 340, 123, 46]
    result       = []
    bitmap = Bitmap(MAX)
    for num in suffle_array:
        bitmap.set(num)

    for i in range(MAX + 1):
        if bitmap.test(i):
            result.append(i)

    print '原始数组为:    %s' % suffle_array
    print '排序后的数组为: %s' % result