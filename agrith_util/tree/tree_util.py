#!/usr/bin/env python
# coding=utf-8
from comm_util import *
class TreeNode:
    data =''
    count = 0
    childNode=[]*26
    def __init__(self,datax,childx=None):
        self.data = datax
        self.childNode = childx
        
def create_tree(tree,c):
    print '-building tree-'
    childNodes = tree.childNode
    exist_node = False
    for _node in childNode:
        if _node.data == c:
            node = TreeNode()
'''
demo
node=[0]='' [1]=-1  [2]=-1  [3]=[]         [4]=[] 
    ------------------------------------------------------
    data    id      parent  left_children  right_children
    
    tree = ['root',1,-1,   [],          []]
    |------data   id pid left_children,right_children
    node=tree[i]
    data = node[0]
    id=node[1]
    parentid=node[2]
    left_children = node[3]
    right_children = node[4]
'''
#tree = [{'data':'root','id':1,'parent':-1,'left_children':[],'right_children':[]}]
#tree = ['root',1,-1,[],[]]
def tree_len(tree):
    return len(tree)
def add_node(tree,id,parent,data):
    #new_node = {'data':'','id':0,'parent':0,'left_children':[],'right_children':[]}
    #new_node = ['root',1,-1,[],[]]
    new_node = [data,id,parent,[],[]]
    """
    last_index = tree_length(tree)-1
    new_index = last_index+1
    new_node['id'] = new_index
    new_node['data'] = data
    new_node['parent'] = parent
    """

    parent_node = tree[parent]
    left_children = parent_node[3]
    right_children = parent_node[4]

    # right node
    if len(tree) % 2 == 0:
        right_children.append(id)  
    # left node
    else:
        left_children.append(id)  
    parent_node[3] = left_children
    parent_node[4] = right_children
    tree.append(new_node)
def build_tree(tree,list):
    for _i,_e in enumerate(list):
        parent =0
        # parent 0 - i=0 / i=1 
        if _i ==1 or _i ==0:
            parent =0
        else:
            if _i % 2==0:
                parent = _i/2
            else:
                parent = (_i-1)/2
        #print parent
        
        add_node(tree,_i+1,parent,_e)
def build_sub_tree(tree,nodeIdList):
    print '--sub_tree-',tree,nodeIdList
    new_tree = []
    for _i in nodeIdList:
        print _i
        new_tree.append(tree[_i])
    return new_tree
def print_tree(tree):
    if len(tree)>0:
        data = node[0]
        left_children = node[3]
        right_children=node[4]
        if len(left_children) == 0:
            print 'data:',data
            return
        else:
            sub_tree = build_sub_tree(tree,left_children)

# - bad
def depth_order(tree):
    print 'depth_order'
    print  tree
    if len(tree)>0:
        node = tree[0]
        print node
        data = node[0]
        left_children = node[3]
        right_children=node[4]
        if len(left_children) == 0:
            print 'data:',data
            return
        else:
            sub_tree = build_sub_tree(tree,left_children)
            depth_order(sub_tree)
    else:
        print 'depth_order over'

def width_order(tree):
    print 'width_order'
if __name__=='__main__':
    print '--main--'
    #tree = []
    """
         root -0
      /         \
    a1a-1      b2b-2
    /    \       /    \
    c3c-3 d4d-4 e5e-5  f6f-6 
    """
    tree = [['root',-1,-1,[],[]]]
    l=['a1a','b2b','c3c','d4d','e5e','f6f']
    build_tree(tree,l)
    print_list(tree)

    #depth_order(tree)
