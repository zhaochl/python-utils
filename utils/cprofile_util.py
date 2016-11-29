#!/usr/bin/env python
# coding=utf-8

def foo1():
    sum = 0
    for i in xrange(100):
        sum += i
    return sum

def foo2():
    sum = 0
    for i in xrange(1000000):
        sum += i
    return sum

def foo3():
    sum = 0
    for i in xrange(10000):
        sum += i
    return sum
def foo():
    foo1()
    foo2()
    foo3()

if __name__ == '__main__':
    import cProfile

    cProfile.run("foo()",'stat')
    import pstats
    p = pstats.Stats('stat')
    #strip_dirs()移除模块名之前的路径信息，sort_stats(-1)按标准名(module/line/name)排序,print_stats打印统计信息
    p.strip_dirs().sort_stats(-1).print_stats()
    #按time排序并显示前10行
    p.sort_stats('time').print_stats(10)
    #按file排序只显示class init方法相关的统计信息
    p.sort_stats('file').print_stats('__init__')
    #先按time排序再按cum排序，只输出50%，然后仅列出包含init的部分
    p.sort_stats('time', 'cum').print_stats(.5, 'init')
    #若想知道谁调用了上述函数可以使用
    p.print_callers(.5, 'init')
