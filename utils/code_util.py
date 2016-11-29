#!/usr/bin/env python
# coding=utf-8
if __name__=='__main__':
    print 'tt'
    s='\u5bf9\u5f00\u53d1\u8005\u548c\u5e7f\u544a\u4e3b\u610f\u4e49\u91cd\u5927'
    #t=s.encode('utf8')
    t=s.decode('raw_unicode_escape')
    print 't1:',t
    s=u'\u5bf9\u5f00\u53d1\u8005\u548c\u5e7f\u544a\u4e3b\u610f\u4e49\u91cd\u5927'
    #t=s.encode('utf8')
    t=s.decode('utf8')
    print 't2:',t

    #s is utf format
    s='人生苦短'
    t=unicode(s,'utf8')
    print 't:',t
    #u decode to unicode
    u=s.decode('utf8')
    print 'u:',u
    #p is u encode to utf8
    p = u.encode('utf8')
    print 'p:',p
    print '*'*10
    
    a='\u5bf9'
    b='u'+a
    print b
    t=b.encode('utf8')
    print t

    print '-'*50
    s='abc'
    #type str
    print s,type(s)
    t=unicode(s)
    #type unicode
    print t,type(t)
