#!/usr/bin/env python
# coding=utf-8
import pstats
import cProfile

def foo():
    sum = 0
    for i in range(10000):
        sum += i
    sumA = bar()
    sumB = bar()
    return sum
     
def bar():
    sum = 0
    for i in range(100000):
        sum += i
    return sum

if __name__ == "__main__":
    cProfile.run("foo()", "result")
    p = pstats.Stats("result")
    p.strip_dirs().sort_stats("cumulative").print_stats(3)
