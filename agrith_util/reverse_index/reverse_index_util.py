'''
reverse_index = [{'key1':[1,2,3]},{'key2':[1,3]}]
'''

def create_reverse_index(l,key,val):
    print 'key:'+key

    if len(l)==0:
        l.append({key: [val]})
        return l

    for _i,_e in enumerate(l):
        print _e
        #for k,v in _e.viewitems():
        #    print "k=%s, v=%s" % (k, v)
        if _e.has_key(key):
            print 'true'
            _e[key].append(val)
            break
        else:
            if _i==(len(l)-1):
                print 'false'
                l.append({key: [val]})
                break
    print_list(l)
    return l
def create_reverse_index_isrepeat(l,key,val,repeat):
    if len(l)==0:
         l.append({key: [val]})
         return l
    for _i,_e in enumerate(l):
        '''
        for key,value in _e.viewitems():
            print "key=%s, value=%s" % (key, value)
        '''
        if _e.has_key(key):
            print 'true'
            if repeat == False:
                print  _e[key]
                if val not in _e[key]:
                    _e[key].append(val)
                    print 'not in'
            else:
                _e[key].append(val)

            break
        else:
            if _i==(len(l)-1):
                print 'false'
                l.append({key: [val]})
                break
    return l
'''
author:chunliang
create date:2015-12-09
description: find the reverse index list for a key
    reverse_index = [{'key1':[1,2,3]},{'key2':[1,3]}]
    search('key1',reverse_index)=[1,2,3]
return: []
'''
def search_reverse_index(key,l):
    result=[]
    for r in l:
        if r.has_key(key):
            result = r[key]
            break
    return result
        #for k,v in r.viewitems():
        #    print "key=%s,value=%s"% (k,v)

#reverse_index = [{'key1':[1,2,3]},{'key2':[1,3]}]
reverse_index=[]
reverse_index=create_reverse_index_isrepeat(reverse_index, 'key1', 4,False)
reverse_index = create_reverse_index_isrepeat(reverse_index, 'key3', 55,False)
reverse_index =create_reverse_index_isrepeat(reverse_index, 'key3', 55,False)
print reverse_index
print '--------------------------------------------------'
def print_list(l):
    print '---print list info start--'
    for _l in l:
        print _l
    print '--print list info end---'
def print_reverse_index(l):
    print '---print list info start--'
    for _l in l:
        #print _l
        for k,v in _e.viewitems():
            print "k=%s, v=%s" % (k, v)
    print '--print list info end---'
reverse_index = [{'key1':[1,2,3]},{'key2':[1,3]}]
#reverse_index=[]
reverse_index=create_reverse_index(reverse_index, 'key1', 4)
reverse_index = create_reverse_index(reverse_index, 'key3', 55)
reverse_index =create_reverse_index(reverse_index, 'key3', 5)
reverse_index =create_reverse_index(reverse_index, 'key3', 5)
reverse_index =create_reverse_index(reverse_index, 'key3', 6)
print reverse_index

#----------------------test--
#id    username    password
table_index_dict={'101':'101_u1_p1','102':'101_u2_p2'}
table_index_dict[103]='103_u3_p3'
print table_index_dict
