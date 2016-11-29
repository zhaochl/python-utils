#!/usr/bin/env python
# coding=utf-8
from pdb import *

seg_dict = ['你好','中国','国庆','节','节日','快乐']

def load_dict():
    d = {}
    for r in seg_dict:
        r = unicode(r)
        d[r] =1
    return d

def split_term(sentence):
    sentence = unicode(sentence)
    d = load_dict()
    word_total = len(sentence)
    word_index = 0
    w_last =''
    terms_list =[]
    #set_trace()
    for w in sentence:
        word_index +=1

        if d.has_key(w):
            terms_list.append(w)
            w_last = ''
        else:
            if w_last=='':
                w_last=w
            else:
                w_last+=w
                if d.has_key(w_last):
                    terms_list.append(w_last)
                    w_last = w_last[1:]
                else:
                    if len(w_last)>=3:
                        w_last = w_last[1:]
    if word_index== word_total and len(terms_list)>0:
        print 'split_term failed'
    return terms_list
if __name__=='__main__':
    s='国庆节快乐'
    terms_list = split_term(s)
    for r in terms_list:
        print r
