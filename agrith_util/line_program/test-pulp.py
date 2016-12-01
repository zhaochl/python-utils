#!/usr/bin/env python
# coding=utf-8
from pulp import *

def test():
    prob = LpProblem('lptest', LpMaximize)
    x1 = LpVariable('x1', lowBound = 0)
    x2 = LpVariable('x2', lowBound = 0)
    prob += 2 * x1 + 5 * x2
    prob += 2 * x1 - x2 <= 4
    prob += x1 + 2 * x2 <= 9
    prob += -x1 + x2 <= 3
    GLPK().solve(prob)
    for v in prob.variables():
        print v.name, '=', v.varValue
        print 'objective =', value(prob.objective)

if __name__=='__main__':
    test()
