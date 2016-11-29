#!/usr/bin/env python
# coding=utf-8
import pygraphviz as pgv
from pdb import *
def small_tree():
    myTree = ['a', ['b', ['d',[],[]], ['e',[],[]] ], ['c', ['f',[],[]], []] ]
    print(myTree)
    print 'left subtree:', myTree[1]
    print 'root:', myTree[0]
    print 'right subtree:', myTree[2]
"""
data='a'
"""
def create_tree(t,data=None):
    #set_trace()
    root =[]
    node=[data,[],[]]
    if len(t)==0:
        root.append(node)
        t=root
        return t
    else:
        root = t[0]
    queue =[]
    queue.append(root)
    while queue:
        tree_node = queue.pop(0)
        if tree_node[1]==[]:
            tree_node[1]=node
            return t 
        elif tree_node[2]==[]:
            tree_node[2]=node
            return t
        else:
            queue.append(tree_node[1])
            queue.append(tree_node[2])
    return t
def level_order_tree(t,A):
    if len(t)==0:
        return []
    root=t[0]
    queue =[]
    queue.append(root)
    parent_data=root[0]
    while queue:
        tree_node = queue.pop(0)
        node_data = tree_node[0]
        
        print node_data
        add_graph_tree(A,parent_data,node_data)
        parent_data = node_data
        #right
        if tree_node[2]!=[]:
            queue.append(tree_node[2])
        #left
        if tree_node[1]!=[]:
            queue.append(tree_node[1])
    return A
def pre_order_tree(root,parent_data,A):
    if t==[]:
        return
    node_data = root[0]
    left = root[1]
    #print left
    right = root[2]
    #print right
    #print data
    if A!=None:
        add_graph_tree(A,parent_data,node_data)
        parent_data = node_data
    else:
        print node_data
    if left!=[]:
        pre_order_tree(left,node_data,A)
    if right!=[]:
        pre_order_tree(right,node_data,A)
    return A
def add_graph_tree(A,edge_start,edge_end):
    A.add_edge(edge_start,edge_end)
    return A
def graph_tree_main(t):
    A=pgv.AGraph(directed=True,strict=True)
    #A = level_order_tree(t,A)
    root=t[0]
    root_data = root[0]
    A= pre_order_tree(root,root_data,A)
    print A
    A.graph_attr['epsilon']='0.001'
    print A.string() # print dot file to standard output
    A.write('tree.dot')
    A.layout('dot') # layout with dot
    A.draw('tree.png') # write to file
    print 'success'
def graph_tree_test():
    A=pgv.AGraph(directed=True,strict=True)
    A.add_edge(1,2)
    A.add_edge(1,3)
    A.add_edge(2,4)
    A.add_edge(2,5)
    A.add_edge(5,6)
    A.add_edge(5,7)
    A.add_edge(3,8)
    A.add_edge(3,9)
    A.add_edge(8,10)
    A.add_edge(8,11)
    A.graph_attr['epsilon']='0.001'
    print A.string() # print dot file to standard output
    A.write('tree.dot')
    A.layout('dot') # layout with dot
    A.draw('tree.png') # write to file
    print 'success'
if __name__=='__main__':
    #small_tree()
    t=[]
    data_list = range(1,11)
    for d in data_list: 
        t=create_tree(t,d)
    #print t
    #graph_tree_test()
    #level_order_tree(t)
    graph_tree_main(t)
    
    #root = t[0]
    #root_data = root[0]
    #pre_order_tree(root,root_data,None)
