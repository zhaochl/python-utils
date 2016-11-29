#!/usr/bin/env python
# coding=utf-8

#
# userIdNeighborsTopk=sorted(userIdSimHash.items(), lambda x, y: cmp((x[1]), (y[1])), reverse=True)[0:realtopk]
#
"""
key=k,v,
k mean sorted by key
v mean sorted by value
k = cmp as string
v = cmp as float
"""
def sort_dict(d,key,order):
    reverse = True
    if order=='asc':
        reverse = False
    elif order=='desc':
        reverse = True
    _results = []
    order_index=1
    if d!=None:
        if key =='v':
            order_index=1
        elif key =='k':
            order_index=0
        else:
            print 'sort_dict - wrong parameters'
            exit(1)
        _results_tmp = None
        if key=='v':
            _results_tmp =sorted(d.iteritems(),cmp=lambda x,y:cmp(float(x[order_index]),float(y[order_index])),reverse=reverse)
        elif key=='k':
            _results_tmp =sorted(d.iteritems(),cmp=lambda x,y:cmp(x[order_index],y[order_index]),reverse=reverse)

        for _k,_v in _results_tmp:
            _t = {_k:_v}
            _results.append(_t)
    return _results

"""
key=k,v,
k mean sorted by key
v mean sorted by value
k = cmp as string
v = cmp as float
"""
def sort_dict_topN(d,key,order,topn=10):
    reverse = True
    if order=='asc':
        reverse = False
    elif order=='desc':
        reverse = True
    _results = []
    order_index=1
    if d!=None:
        if key =='v':
            order_index=1
        elif key =='k':
            order_index=0
        else:
            print 'sort_dict - wrong parameters'
            exit(1)
        _results_tmp = None
        if key=='v':
            _results_tmp =sorted(d.iteritems(),cmp=lambda x,y:cmp(float(x[order_index]),float(y[order_index])),reverse=reverse)
        elif key=='k':
            _results_tmp =sorted(d.iteritems(),cmp=lambda x,y:cmp(x[order_index],y[order_index]),reverse=reverse)
        _topn = topn
        if len(_results_tmp)<topn:
            _topn = len(_results_tmp)
        _count = 0
        for _k,_v in _results_tmp:
            if _count<_topn:
                _t = {_k:_v}
                _results.append(_t)
                _count+=1
            else:
                break
    return _results

def get_dict_val_min_topn(d,topn):
    return sort_dict_topN(d,'v','asc',topn)

def get_dict_val_max_topn(d,topn):
    return sort_dict_topN(d,'v','desc',topn)
"""
reverse=False 升序
reverse=True 升序
"""
def sort_list(l,reverse=False):
    l.sort(reverse=reverse)
    return l
if __name__=='__main__':
    print '-test sort-'

    a={'b':0.21,'a':0.3,'c':0.5}

    print '----order by key desc---'
    t=sort_dict(a,'k','desc')
    print t
    
    print '----order by key asc---'
    t=sort_dict(a,'k','asc')
    print t
    
    print '----order by val desc---'
    t=sort_dict(a,'v','desc')
    print t
    
    print '----order by val asc---'
    t=sort_dict(a,'v','asc')
    print t
    
    print '----order by val desc,get topn---'
    t=sort_dict_topN(a,'v','desc',2)
    print t
    
    print '----get_dict_val_min_topn---'
    t=get_dict_val_min_topn(a,2)
    print t
    print '----get_dict_val_max_topn---'
    t=get_dict_val_max_topn(a,2)
    print t


    a=[4,5,3,6]
    t= sort_list(a)
    print t
    a=[4,5,3,6]
    t= sort_list(a,True)
    print t
