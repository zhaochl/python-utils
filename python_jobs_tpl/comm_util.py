#!/usr/bin/python
# -*- coding: utf-8 -*-
Debug=0
def dp(debug,content):
    if debug==1:
        print str(content)
def print_list(l):
    print '---print list info start--'
    for _l in l:
        print _l
    print '--print list info end---'
def print_dict(d):
    print '---print dict info start--'
    for key,value in d.viewitems():
        print "key=%s, value=%s" % (key, value)
    print '---print dict info end--'
def print_reverse_index(l):
    print '---print reverse info start--'
    for _e in l:
        #print _l
        for k,v in _e.viewitems():
            print "k=%s, v=%s" % (k, v)
    print '--print reverse index info end---'
def die():
    exit(1)

if __name__=='__main__':
    print 'demo main.'
    dp(1,'--dp test--')
    dp(2,'--nothing to show--')
