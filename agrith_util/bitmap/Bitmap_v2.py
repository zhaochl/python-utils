#!/usr/bin/env python
#coding: utf8


#http://my.oschina.net/goal/blog/200347

class Bitmap(object):
    def __init__(self, max):
        self.size  = self.calcElemIndex(max, True)
        self.array = [0 for i in range(self.size)]

    '''
    计算在数组中的索引
    '''
    def calcElemIndex(self, num, up=False):
        '''up为True则为向上取整, 否则为向下取整'''
        if up:
            return int((num + 31 - 1) / 31) #向上取整
        return num / 31
    '''
    计算在数组元素中的位索引
    '''
    def calcBitIndex(self, num):
        return num % 31
    '''
    二进制位默认是0，将某位置1则表示在此位存储了数据
    '''
    def set(self, num):
        elemIndex = self.calcElemIndex(num)
        byteIndex = self.calcBitIndex(num)
        elem      = self.array[elemIndex]
        print 'elem:'+str(elem)+',byteIndex:'+str(byteIndex)+',elemIndex:'+str(elemIndex)
        self.array[elemIndex] = elem | (1 << byteIndex)
    '''
    将某位置0，也即丢弃已存储的数据
    '''
    def clean(self, i):
        elemIndex = self.calcElemIndex(i)
        byteIndex = self.calcBitIndex(i)
        elem      = self.array[elemIndex]
        self.array[elemIndex] = elem & (~(1 << byteIndex))
    '''
    判断某位是否为1是为了取出之前所存储的数据
    '''
    def test(self, i):
        elemIndex = self.calcElemIndex(i)
        byteIndex = self.calcBitIndex(i)
        if self.array[elemIndex] & (1 << byteIndex):
            return True
        return False
if __name__ == '__main__':
    #10亿
    #bitmap = Bitmap(1000*1000*1000)
    #print '数组需要 %d 个元素。' % bitmap.size
    #32258065

    bitmap = Bitmap(90)
    print '数组需要 %d 个元素。' % bitmap.size
    print '47 应存储在第 %d 个数组元素上。' % bitmap.calcElemIndex(47)
    print '47 应存储在第 %d 个数组元素的第 %d 位上。' % (bitmap.calcElemIndex(47), bitmap.calcBitIndex(47),)

    #--test clean--
    bitmap.set(0)
    bitmap.set(34)
    print bitmap.array
    bitmap.clean(0)
    print bitmap.array
    bitmap.clean(34)
    print bitmap.array

    #---test-set--
    bitmap.set(2)
    for b in bitmap.array:
        print bin(b)[2:]
    #--test-test--
    bitmap.set(1)
    print bitmap.test(1)
    bitmap.clean(1)
    print bitmap.test(1)