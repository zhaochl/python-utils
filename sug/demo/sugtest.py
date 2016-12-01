#!/usr/bin/env python
# coding=utf-8
from tree_builder import *
from tire_tree import *

if __name__ == '__main__':
    build_tree()
    infile = open('test.dat')
    outfile = open('result.txt', 'w')
    for term in infile.readline():
        sugs = get_suggestion(term)
        outfile.write(term+'\n')
        for sug in sugs:
            outfile.write(sug+'    ')
        outfile.write('\n')

    infile.close()
    outfile.close()
