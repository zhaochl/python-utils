#!/usr/bin/env python
# coding=utf-8
from data_util import *
from tire_tree import *
from constant import *
import pygraphviz as pgv
import json
import os

PROJECT_BATCH_SIZE = 100

def build_tree(pid = 0):
    while True:
        projs = DataUtil.get_project_term(pid, PROJECT_BATCH_SIZE)

        for proj in projs:
            title = proj[0]
            category = proj[1].split()
            keywords = proj[2].split()
            brief = proj[3].split()
            pid = proj[4]
            projectid = proj[5]
            info = DataUtil.get_project_info(projectid)

            terms = {}

            terms[title] = 1.0
            for i in range(len(category)/2):
                term = category[i*2].split('=')[1]
                weight = category[i*2+1].split('=')[1]
                if term[1] == '_':
                    term = term[2:]
                weight = float(weight)
                terms[term] = weight

            for i in range(len(keywords)/2):
                term = keywords[i*2].split('=')[1]
                weight = keywords[i*2+1].split('=')[1]
                if term[1] == '_':
                    term = term[2:]
                weight = float(weight)
                terms[term] = weight

            for e in info:
                name = e[0]
                terms[name] = 1.0

            for term, weight in terms.iteritems():
                if len(unicode(term)) == 1:
                    continue
                if len(str(term))==len(unicode(term)) and len(str(term))==2:
                    continue
                add_term(term, weight)

        if len(projs) < PROJECT_BATCH_SIZE:
            break

    treefile = open('tree_nodes.txt', 'w')
    indexfile = open('tree_index.txt', 'w')
    treefile.write(json.dumps(tree_nodes))
    indexfile.write(json.dumps(node_index))
    treefile.close()
    indexfile.close()

def build_tree_test():
    for action in CONST_ACTION_LIST:
        uni_action = unicode(action)
        add_term(uni_action,1.0)

    treefile = open('tree_nodes.txt', 'w')
    indexfile = open('tree_index.txt', 'w')
    treefile.write(json.dumps(tree_nodes))
    indexfile.write(json.dumps(node_index))
    treefile.close()
    indexfile.close()



def load_tree():
    if not os.path.exists('tree_nodes.txt') or not os.path.exists('tree_index.txt'):
        build_tree_test()
        return
        
    global tree_nodes
    global node_index
    treefile = open('tree_nodes.txt')
    indexfile = open('tree_index.txt')
    tree_nodes.pop()#pop root node
    tree_nodes += json.loads(treefile.read())
    index = json.loads(indexfile.read())
    for key, nid in index.iteritems():
        node_index[key] = nid
    treefile.close()
    indexfile.close()


def graph_tree(graph, parent):
    graph_word1 = str(parent) + tree_nodes[parent][KEYWORD]
    for child in tree_nodes[parent][CHILDREN]:
        graph_word2 = str(child) + tree_nodes[child][KEYWORD]
        graph.add_edge(graph_word1, graph_word2)
        graph_tree(graph, child)
    
def get_graph(parent=0):
    graph = pgv.AGraph(directed=True, strict=True)
    graph_tree(graph, parent)
    graph.graph_attr['epsilon'] = '0.001'
    print graph.string()

    graph.write('tree.dot')
    graph.layout('dot')
    graph.draw('tree.png')


if __name__ == '__main__':
    load_tree()
    sugs = get_suggestion('155')
    for sug in sugs:
        print sug
