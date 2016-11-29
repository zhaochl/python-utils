#!/usr/bin/env python
# coding=utf-8
from graph_util import *

def init_grah():
    graph ={}
    #node_list =['A','B','C','D','E','T']
    node_list =['A','B','C','D','E']
    add_nodes(graph,node_list)
    #print graph
    add_node(graph,'A','B')
    add_node(graph,'A','C')
    add_node(graph,'A','D')
    add_node(graph,'B','D')
    add_node(graph,'C','E')
    add_node(graph,'D','E')
    add_node(graph,'B','E')
    add_node(graph,'E','A')
    #print graph
    #gen_graph_png(graph,'./static/test.png',False)
    print 'ok'
    return graph
def page_rank(graph):
    damping_factor = 0.85  # 阻尼系数,即α
    max_iterations = 100  # 最大迭代次数
    min_delta = 0.00001  # 确定迭代是否结束的参数,即ϵ
     #  先将图中没有出链的节点改为对所有节点都有出链
    all_nodes = get_nodes(graph)
    for node in all_nodes:
        neighbour_list = graph[node]
        if len(neighbour_list)==0:
            print '--leaf node:',node
            for node_out in all_nodes:
                add_node(graph,node,node_out)

    #gen_graph_png(graph,'./static/test1.png',False)
    node_nums = len(all_nodes)
    node_rank = dict.fromkeys(all_nodes, 1.0 /node_nums)  # 给每个节点赋予初始的PR值
    damping_value = (1.0 - damping_factor) / node_nums  # 公式中的(1−a)/N部分
    
    print node_rank
    print damping_value
    #PR(node_x) = a(PR(node_in_y)/node_in_y_out_num) +(1-a)/node_nums
    change = 0
    for i in range(max_iterations):
        for node in all_nodes:
            rank = 0
            in_node_list = find_from_path(graph,node)
            for in_node in in_node_list:
                in_node_neighbor_list = graph[in_node]
                rank += damping_factor *(node_rank[in_node]/len(in_node_neighbor_list))
            rank += damping_value
            change += abs(node_rank[node] - rank)
            node_rank[node] = rank
        #print 'iteration time:%s' %(i+1)
        if change < min_delta:
            break
    print node_rank
if __name__=='__main__':
    url='http://www.cnblogs.com/rubinorth/p/5799848.html'
    print 'learn from url:',url
    g = init_grah()
    t = page_rank(g)
