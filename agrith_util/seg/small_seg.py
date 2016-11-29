#!/usr/bin/env python
# coding=utf-8
from pdb import *

def add(tree,word):
    for char in word:
        if tree.has_key(char):
            tree = tree[char]
        else:
            tree[char] = {}
            tree = tree[char]
    tree['exist'] = True

def search(tree,word):
    print word
    for char in word:
        if tree.has_key(char):
            tree = tree[char]
        else:
            return False
    #print tree
    if tree.has_key('exist'):
        return True
    else:
        return False

def is_empty_tree(tree):
    if len(tree)==0:
        return True
    if len(tree)==1 and tree.has_key('exist'):
        return True
    return False
def depth_order_tree(tree,root):
    tree_path = []
        
    queue =[]
    queue.append(root)
    while queue:
        tree_node = queue.pop(0)
        if tree.has_key(tree_node) and tree_node!='exist':
            tree_path.append(tree_node)
            subtree = tree[tree_node]
            #print tree_node,subtree
            if not is_empty_tree(subtree):
                #set_trace()
                for _sub_node in subtree.keys():
                    if _sub_node!='exist':
                        queue.append(_sub_node)
                tree = subtree
    return tree_path
def suggestion(tree,start_word):
    path=[]
    print start_word
    match_len=0
    match_word=''
    for char in start_word:
        if tree.has_key(char):
            match_len+=1
            match_word+=char
            if match_len!=len(start_word):
                path.append(match_word)
            else:
                depth_order_tree_path = depth_order_tree(tree,char)
                for _path in depth_order_tree_path:
                    path.append(_path)
            tree = tree[char]

        else:
            path.append(tree[char].keys())
            break
    return path
if __name__=='__main__':
    tree = {}
    add(tree,'a')
    add(tree,'ab')
    add(tree,'abcd')
    add(tree,'d')
    add(tree,'dc')
    add(tree,'dcef')
    add(tree,'de')
    print tree
    print '--search---'
    print search(tree,'a')
    print search(tree,'ac')
    print search(tree,'abcd')
    print search(tree,'dc')
    print '--suggestion---'
    print suggestion(tree,'a')
    print suggestion(tree,'abcd')
    print '--depth_order_tree--'
    print depth_order_tree(tree,'d')
