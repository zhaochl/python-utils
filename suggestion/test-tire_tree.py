#!/usr/bin/env python
# coding=utf-8
from tire_tree import *

if __name__=='__main__':
    '''
node|[0]    |[1]   |[2]  |[3]   |[4] |[5]  |[6]    |[7]
----|-------|------|-----|------|----|-----|-------|-------
    |keyword|weight|mtime|parent|type|level|weight2|children
note: only leaf node has weight and mtime, other node's is 0 and 0
'''
    term = '我的祖国'
    add_term('我的祖国', 1)
    #add_term('我的世界', 2)
    #add_term('我的shi姐', 3)
    #for r in tree_nodes:
    #    print r
    
    term = 'nishi我的祖国011abc'
    #term = 'nishi'
    #term = '1112'

    words,types = term2words(term,True)
    print words
    print types
