#!/usr/bin/env python
# coding=utf-8
import pygraphviz as pgv
from pdb import *
gdata = [
    ['A', '->', 'B',1],
    ['A', '->', 'C',1],
    ['B', '->', 'C',1],
    ['B', '->', 'D',1],
    ['C', '->', 'D',1],
    ['D', '->', '',1],
]

graph = {
    'A': ['B', 'C'],
    'B': ['C', 'D'],
    'C': ['D'],
    'D':[]
}
def gen_edge_relations(graph):
    graph_edge = {}
    for node,neighbour_list in graph.iteritems():
        node_relations = {}
        for nb in neighbour_list:
            node_relations[nb] = 1
        #print node,neighbour_list,node_relations

        if not graph_edge.has_key(node):
            graph_edge[node] = node_relations
    return graph_edge
def check_is_edge(graph_edge,_from,_to):
    is_edge = False
    if len(graph_edge)>0:
        if graph_edge.has_key(_from):
            node_relations = graph_edge[_from]
            if node_relations.has_key(_to):
                is_edge = True
    return is_edge

def width_order_graph(graph):    
    graph_edge = gen_edge_relations(graph)
    def BFS(node):
        print(node)
        visited[node] = 1
        for _node,_node_relations in graph.iteritems():
            if check_is_edge(graph_edge,node,_node) and not visited.has_key(_node):
                BFS(_node)

    visited = {}
    #set_trace()
    for node,node_relations in graph.iteritems():
        
        if not visited.has_key(node):
            print 'start BFS:',node
            BFS(node)
    print visited             

    
def depth_order_graph(graph):
    graph_edge = gen_edge_relations(graph)
    def DFS(node,queue):
         
        queue.append(node) 
        print(node)
        visited[node] = 1
        if len(queue) != 0:
            q_node = queue.pop()
            for _node,_node_relations in graph.iteritems():
                if check_is_edge(graph_edge,q_node,_node) and not visited.has_key(_node):
                    DFS(_node, queue)
    
    visited = {}
    queue = []
    for node,node_relations in graph.iteritems():
        if not visited.has_key(node):
            DFS(node,queue)

def build_graph(data):
    graph = {}
    for r in gdata:
        _from = r[0]
        to = r[2]
        status = r[3]
        if status!=1:
            continue
        if _from=='D':
            set_trace()
        if not graph.has_key(_from):
            graph[_from] = [to]
        else:
            graph[_from].append(to)
    return graph


def add_node(graph,_from,to):
    #set_trace()
    if len(graph)>0:
        if not graph.has_key(_from):
            graph[_from] = [to]
        else:
            graph[_from].append(to)
        #fix add leaf node 
        if not graph.has_key(to):
            graph[to] = []
    else:
        graph[_from] =[to]
    return graph



def del_node(graph,_from,to):
    if len(graph)>0:
        #del edge
        if graph.has_key(_from):
            graph[_from].remove(to)
            #del to -if leaf
            if graph.has_key(to):
                t =  graph[to]
                if len(t)==0:
                    graph.pop(to)
    return graph

def find_path(graph, start, end, path=[]):
        path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in path:
                newpath = find_path(graph, node, end, path)
                if newpath: 
                    return newpath
        return None

def find_path2 (graph, start, end, path=[]):
        _path = path + [start]
        if start == end:
            return path
        if not graph.has_key(start):
            return None
        for node in graph[start]:
            if node not in _path:
                newpath = find_path(graph, node, end, _path)
                if newpath: 
                    return newpath
        return None

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if not graph.has_key(start):
        return []
    paths = []
    for node in graph[start]:
        if node not in path:
            newpaths = find_all_paths(graph, node, end, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths
"""
find from ->to ,[from]->from_list
"""
def find_from_path(graph,to):
    path = []
    graph_edge = gen_edge_relations(graph)
    for node,node_relations in graph_edge.iteritems():
        if node_relations.has_key(to):
            path.append(node)
    return path
"""
find x->from ->to ,[from]+[x]->from_list
"""
def find_from_path_all(graph,to,path=[]):
    if to not in path:
        path = path+[to]
    #print path,to in path
    graph_edge = gen_edge_relations(graph)
    for node,node_relations in graph_edge.iteritems():
        if node_relations.has_key(to):
            if not node in path:
                path.append(node)
            find_from_path_all(graph,node,path)
    return path
    
"""
find x->from ->to ,[from]+[x]->from_list
"""
def find_from_path_all_depth_order_graph(graph,to):
    graph_edge = gen_edge_relations(graph)
    def DFS(node,queue):
        queue.append(node) 
        #print(node)
        if len(queue) != 0:
            q_node = queue.pop()
            for _node,_node_relations in graph_edge.iteritems():
                if _node_relations.has_key(q_node) and not visited.has_key(_node):
                    visited[_node] = 1
                    #visited[_node] = 1
                    DFS(_node, queue)
    
    visited = {}
    queue = []
    node = to
    DFS(node,queue)
    return visited
"""
find x->from ->to ,[from]+[x]->from_list
"""
def find_to_path_all_depth_order_graph(graph,_from):
    def DFS(node,queue):
        queue.append(node) 
        print(node)
        visited[node]=1
        if len(queue) != 0:
            q_node = queue.pop()
            for neighbour in  graph[q_node]:
                queue.append(neighbour)
                #if graph.has_key(neighbour) and not visited.has_key(neighbour):
                if graph.has_key(neighbour):
                    DFS(neighbour,queue)
    
    visited = {}
    queue = []
    node = _from
    DFS(node,queue)
    return visited

def find_shortest_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    shortest = None
    for node in graph[start]:
        if node not in path:
            newpath = find_shortest_path(graph, node, end, path)
            if newpath:
                if not shortest or len(newpath) < len(shortest):
                    shortest = newpath
    return shortest

def gen_graph_png(graph,file_name):
    A=pgv.AGraph(directed=True,strict=True)
    for node,node_relations_list in graph.iteritems():
        for neighbour in node_relations_list:
            A.add_edge(node,neighbour)
    
    A.graph_attr['epsilon']='0.001'
    print A.string() # print dot file to standard output
    A.write(file_name+'.dot')
    A.layout('dot') # layout with dot
    A.draw(file_name+'.png') # write to file
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

def test_find(graph):
    print '--find A-E one path--'
    t= find_path(graph, 'A', 'E')    
    print t
    t= find_path2(graph, 'A', 'E')    
    print t
    print '--find A-E all paths-'
    t = find_all_paths(graph, 'A', 'E')
    print t
    print '--find A-E short path-'
    t= find_shortest_path(graph, 'A', 'E')
    print t
def test_find_from_path(graph):
    print '--find from node directly--'
    t=find_from_path(graph,'D')
    print t
    print '--find_from_path_all--'
    t = find_from_path_all(graph,'D')
    print t
    
    t = find_from_path_all_depth_order_graph(graph,'D')
    print t
    t = find_to_path_all_depth_order_graph(graph,'A')
    print t
    print graph
def test_update(graph):
    graph = add_node(graph,'D','E')
    print graph
    """
    {'A': ['B', 'C'], 'C': ['D'], 'B': ['C', 'D'], 'D': ['E']}
    """
    print '--add_node-E-F-'
    graph = add_node(graph,'E','F')
    print '--del_node leaf-E-F'
    del_node(graph,'E','F')
    print graph

    print '--del_node leaf-C-D'
    del_node(graph,'C','D')
    print graph

    print '--del_node leaf-B-D'
    del_node(graph,'B','D')
    print graph
    depth_order_graph(graph)
def test_order(graph):
    print '--width_order_graph--'
    width_order_graph(graph)
    print '--depth_order_graph--'
    depth_order_graph(graph)
def test_utils(graph):
    g = build_graph(gdata)
    print g
    print '--gen all graph_edge relations-'
    graph_edge = gen_edge_relations(graph)
    print graph_edge
    print '--check_is_edge--'
    t= check_is_edge(graph_edge,'A','B')
    print t

if __name__=='__main__':
    
    #test_find_from_path(graph)
    #graph_tree_test()
    gen_graph_png(graph,'test')
