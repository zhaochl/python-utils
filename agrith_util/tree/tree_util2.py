#!/usr/bin/env python
# coding=utf-8
from Queue import Queue
from Stack import Stack
# 1-2 1-3
# 2-3
# 3-4
# 4-null
#input 123 -> 123
"""
                1
            /       \
            2         3
            /       / \ \
            5       4  6 7
                    /
                    8
depth_all_path(0)    
[[0, 1, 3, 7], [0, 1, 3, 6], [0, 1, 3, 4, 8], [0, 1, 2, 5]]
depth_all_path(3)    
[[3, 7], [3, 6], [3, 4, 8]]
"""
tree = [[0,[1]],[1,[2,3]],[2,[5]],[3,[4,6,7]],[4,[8]],[5,[]],[6,[]],[7,[]],[8,[]]]
CHILDS_POSITION=1
def init_tree(childs_pos):
    CHILDS_POSITION = childs_pos
def get_childIds(id):
    childs =  tree[id][CHILDS_POSITION]
    return childs
def width_order(queue,id):
    print 'width matching..',id
    childs =  tree[id][CHILDS_POSITION]
    if len(childs)==0:
        print 'end'
    else:
        for _id in childs:
            queue.put(_id)
        while not queue.empty():
            subId = queue.get()
            #print'subId:',subId
            width_order(queue,subId)
def depth_order(stack,id):
    print 'depth matching..',id
    childs =  tree[id][CHILDS_POSITION]
    if len(childs)==0:
        print 'end'
    else:
        for _id in childs:
            stack.push(_id)
        while not stack.isEmpty():
            subId = stack.pop()
            #print'subId:',subId
            depth_order(stack,subId)

def depth_order2(stack,id):
    print 'depth2 matching..',id
    path_stack = Stack()
    path_stack.push(id)
    if is_leaf(id):
        print id,' is leaf,end'
    else:
        stack.push(id)
        while not stack.isEmpty():
            subId = stack.pop()
            print'subId:',subId
            childs =  tree[subId][CHILDS_POSITION]
            for _id in childs:
                depth_order2(stack,_id)
                #stack.push(_id)
            #stack.show()
"""
get all path to leafs
return [[1,3,5],[2,3]]
"""
def depth_all_path(id):
    print '-'*100+'depth_all_path matching..',id
    all_path = []

    #done visited path
    path_stack = Stack()
    #undo unvisited stack
    stack = Stack()
    stack.push(id)
    while not stack.isEmpty():
        subId = stack.pop()
        #print'subId:',subId
        if is_leaf(subId):
            #print subId,' is leaf,end'
            path_stack.push(subId)
            #path_stack.show()
            leaf_path = path_stack.build_list()
            all_path.append(leaf_path)
            #all_path.append(path_stack.data())

            path_stack = rebuild_path_stack(path_stack,stack)
            #print '---after rebuild---'
            #path_stack.show()
            #stack.show()
        else:
            path_stack.push(subId)
            childs =  tree[subId][CHILDS_POSITION]
            for _id in childs:
                #depth_order2(stack,_id)
                stack.push(_id)
            #stack.show()
    #print all_path
    return all_path
def rebuild_path_stack(path_stack,stack):
    #print '---rebuild -before--'
    #path_stack.show()
    #stack.show()
    build_over = False
    while not path_stack.isEmpty() and not build_over:
        subId = path_stack.pop()
        #print 'test node subId:',subId
        if is_leaf(subId):
            #print 'leaf,not has'
            continue
        else:
            childs =  tree[subId][CHILDS_POSITION]
            #print 'childs:',childs
            for _id in childs:
                if stack.contains(_id):
                    # - re put parentId
                    path_stack.push(subId)
                    # - re put undo childs
                    # path_stack.push(_id)
                    build_over = True
                    #print 'has'
                    break
                else:
                    #print 'not has'
                    pass

    #print '---rebuild -end--'
    #path_stack.show()
    
    return path_stack
                

def max_len_sub_tree(id):
    print 'max matching..',id
    path_list = depth_all_path(id)
    max_len = 0
    result = []
    for path in path_list:
        if len(path)>max_len:
            max_len = len(path)
            result = path
    return result
def is_leaf(id):
    _results = None
    childs =  tree[id][CHILDS_POSITION]
    if len(childs)==0:
        _results = True
    else:
        _results = False
    return _results

if __name__ =='__main__':
    """
    queue = Queue()
    width_order(queue,0)
    stack = Stack()
    depth_order(stack,0)
    stack = Stack()
    """
    stack = Stack()
    path_list = []
    #depth_order2(stack,0)
    
    #
    t= depth_all_path(3)
    print t

    t=max_len_sub_tree(3)
    print t
