#!/usr/bin/env python
# coding=utf-8
from comm_util import *
from tree_util2 import *
'''
def as database table ddl
--------0-------1------2----3----4
tree = [1    , -1,  'root', 1,  []]
        index parent data,  level  ,childs
'''
# - like one dataset
tree = [[0,-1,'root',1,[]]]

# - 
tree_node = [0,-1,'root',0,[]]

word_rindex = {}
init_tree(4)

def term2words(term):
    term = unicode(term)
    return list(term)
def refresh_rindex(w,new_node_id):
    # add to term_rindex
    if word_rindex.has_key(w):
        word_rindex[w].append(new_node_id)
    else:
        word_rindex[w] = [new_node_id]
def add_term(term):
    words = term2words(term)
    find_road_way = max_prefix_match2(words)
    print 'find_road_way:',find_road_way
    # - add term
    if len(find_road_way) ==0:
        print 'add_term'
        for index,w in enumerate(words):
            new_node_id = len(tree)
            parent_id = 0
            if index > 0:
                parent_id = new_node_id-1
            # - update word_rindex
            refresh_rindex(w,new_node_id)

            #----------------index   parent,word,level 
            child_node_list = []
            # last
            if index==len(words)-1:
                print '---last word:',w
                child_node_list = []
            else:
                child_node_list = []
            tree[parent_id][4].append(new_node_id)
            new_node = [new_node_id,parent_id,w,index+1,child_node_list]
            print 'new_node:',new_node
            tree.append(new_node)
    # - append term
    else:
        print 'append term'
        match_indexed = len(find_road_way)-1
        print 'match_indexed:',match_indexed,'len-find_road_way:',len(find_road_way),'find_road_way:',find_road_way
        last_node_id = find_road_way[match_indexed]
        print 'last_node_id',last_node_id
        last_node = tree[last_node_id]
        match_index_inc = match_indexed+1
        print 'match_index_inc:',match_index_inc
        print '----------before append--'
        print_list(tree)
        print '----------before end'
        #for match_index_inc,w in enumerate(words):
        for match_index in range(match_index_inc,len(words)):
            w = words[match_index]
            print 'try to append,index',match_index_inc,',word:',w
            new_node_id = len(tree)

            parent_id = last_node_id
            # - combine add to append
            if match_index ==match_index_inc:
                parent_id = last_node_id
                tree[parent_id][4].append(new_node_id)
            # - append
            else:
                parent_id = new_node_id-1
                print 'parent_id',parent_id
                print 'new_node_id',new_node_id
                # parent_id -> new subId
                tree[parent_id][4].append(new_node_id)
            level = len(tree)+1
            # add to word_rindex
            if word_rindex.has_key(w):
                word_rindex[w].append(new_node_id)
            else:
                word_rindex[w] = [new_node_id]
            # - update parent -childlist
            #tree[parent_id][4].append(new_node_id)
            #----------------index   parent,word,level 
            child_node_list = []
            # last
            new_node = [new_node_id,parent_id,w,level,child_node_list]
            if new_node_id ==5:
                print 'node-info:',new_node
            tree.append(new_node)

def child_match(node_id,word):
    _result_node_id=-1
    #childs = get_childIds(node_id)
    childs =  tree[node_id][4]
    print 'node_id:',node_id,'childs:',childs
    print tree
    for cnode_id in childs:
        cword = tree[cnode_id][2]
        if cword == word:
            _result_node_id = cnode_id
    return _result_node_id

def max_prefix_match2(words):
    old_node_id=0
    find_road_way = []
    for index,w in enumerate(words):
        print 'matching:',w
        new_node_id = child_match(old_node_id,w)
        if new_node_id==-1:
            break
        else:
            old_node_id=new_node_id
            find_road_way.append(new_node_id)
        """
        if word_rindex.has_key(w):
            word_nodes = word_rindex[w]
            print '\tword_nodes:',word_nodes
            if index+1 in word_nodes:
                print '---matched',index
                find_road_way.append(index+1)

        """


    return find_road_way

    

def max_prefix_match(words):
    level_word_index = 0
    is_last_word = False
    is_find = False
    is_break = False
    find_road_way = []
    for index,w in enumerate(words):
        print 'matching:',w
        if index == len(words)-1:
            print '---1'
            is_last_word = True
            break
        if is_break:
            print '---2'
            break
        if word_rindex.has_key(w):
            word_nodes = word_rindex[w]
            print '\tword_nodes:',word_nodes
            for _node_id in word_nodes:
                _rword_node = tree[_node_id]
                _rword = _rword_node[2]
                _rword_node_child = _rword_node[4]
                print '\t\t_rword_node_child[]:',_rword_node_child
                if len(_rword_node_child)==0:
                    find_road_way.append(_node_id)
                    break
                else:
                    for _rchild_node_id in _rword_node_child:
                        _rchild_word_node = tree[_rchild_node_id]
                        _rword = _rchild_word_node[2]
                        if is_last_word:
                            level_word_index+=1
                            is_find = True
                        elif _rword == words[index+1]:
                            level_word_index+=1
                            print level_word_index
                            find_road_way.append(_node_id)
                        else:
                            is_find = False
    print '\tfind_road_way:',find_road_way
    return find_road_way
    
if __name__=='__main__':
    print 'main'
    
    s='我的祖国'
    l = term2words(s)
    
    #print len(l)
    #for k in l :
    #    print k
    
    #tree = [[0,-1,'root',1,[1]],[1,0,'我',2,[2]],[2,1,'的',3,[3]],[3,2,'祖',],[4,3,'国',4,[4]]]
    #print_list(tree)
    print '*'*100
    add_term('我的祖国')
    print_list(tree)
    print_dict(word_rindex)
    print '-'*50
    add_term('我的母亲')
    add_term('我的母亲爱我')
    add_term('你好')
    print_list(tree)
    print_dict(word_rindex)
