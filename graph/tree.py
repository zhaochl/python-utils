#!/usr/bin/env python
# coding=utf-8
import pygraphviz as pgv
# strict (no parallel edges)
# digraph
# with attribute rankdir set to 'LR'
A=pgv.AGraph(directed=True,strict=True)
A.add_edge(1,2)
A.add_edge(1,3)
A.add_node('a',style='invis')
A.add_edge(1,'a',style='invis')
B=A.add_subgraph([2,3,'a'],rank='same')
B.add_edge(2,'a',style='invis')
B.add_edge('a',3,style='invis')

A.add_edge(2,4)
A.add_edge(2,5)
A.add_node('b',style='invis')
A.add_edge(2,'b',style='invis')
C=A.add_subgraph([4,5,'b'],rank='same')
C.add_edge(4,'b',style='invis')
C.add_edge('b',5,style='invis')

A.add_edge(5,6)
A.add_edge(5,7)
A.add_node('c',style='invis')
A.add_edge(5,'c',style='invis')
D=A.add_subgraph([6,7,'c'],rank='same')
D.add_edge(6,'c',style='invis')
D.add_edge('c',7,style='invis')

A.add_edge(3,8)
A.add_edge(3,9)
A.add_node('d',style='invis')
A.add_edge(3,'d',style='invis')
E=A.add_subgraph([8,9,'d'],rank='same')
E.add_edge(8,'d',style='invis')
E.add_edge('d',9,style='invis')

A.add_edge(8,10)
A.add_edge(8,11)
A.add_node('e',style='invis')
A.add_edge(8,'e',style='invis')
F=A.add_subgraph([10,11,'e'],rank='same')
F.add_edge(10,'e',style='invis')
F.add_edge('e',11,style='invis')


A.graph_attr['epsilon']='0.001'
print A.string() # print dot file to standard output
A.write('tree.dot')
A.layout('dot') # layout with dot
A.draw('tree.png') # write to file
