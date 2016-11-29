#!/usr/bin/env python
# coding=utf-8

import hashlib
def test():
    m = hashlib.md5()   #创建hash对象，md5:(message-Digest Algorithm 5)消息摘要算法,得出一个128位的密文
    print m             #<md5 HASH object @ 000000000254ADF0>
    m.update('BeginMan')#更新哈希对象以字符串参数
    print m.digest()    #返回摘要，作为二进制数据字符串值
    print m.hexdigest() #返回十六进制数字字符串    0b28251e684dfbd9102f8b6f0281c0c5
    print m.digest_size #16
    print m.block_size  #64
    url="http://www.cnblogs.com/BeginMan/p/3328172.html"
    md5 = hashlib.md5(str(url)).hexdigest()
    print md5,len(md5)
    h = hash(url)
    print h,len(str(h))
    url2="http://www.cnblogs.com/BeginMan/p/3328171.html"
    h2 = hash(url2)
    print h2
    
    a=hash('a')
    print a,len(str(a))
    ab=hash('ab')
    print ab,len(str(ab))

if __name__=='__main__':
    test()
