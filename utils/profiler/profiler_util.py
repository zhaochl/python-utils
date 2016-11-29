#!/usr/bin/env python
# coding=utf-8

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
    import cProfile
 
    #直接把分析结果打印到控制台
    cProfile.run("foo()")
    #把分析结果保存到文件中,不过内容可读性差...需要调用pstats模块分析结果
    cProfile.run("foo()", "result")
    #还可以直接使用命令行进行操作
    #>python -m cProfile myscript.py -o result
     
    import pstats
    #创建Stats对象
    p = pstats.Stats("result")
    #这一行的效果和直接运行cProfile.run("foo()")的显示效果是一样的
    p.strip_dirs().sort_stats(-1).print_stats()
    #strip_dirs():从所有模块名中去掉无关的路径信息
    #sort_stats():把打印信息按照标准的module/name/line字符串进行排序
    #print_stats():打印出所有分析信息
 
    #按照函数名排序 
    p.strip_dirs().sort_stats("name").print_stats()
 
    #按照在一个函数中累积的运行时间进行排序
    #print_stats(3):只打印前3行函数的信息,参数还可为小数,表示前百分之几的函数信息
    p.strip_dirs().sort_stats("cumulative").print_stats(3)
 
    #还有一种用法
    p.sort_stats('time', 'cum').print_stats(.5, 'foo')
    #先按time排序,再按cumulative时间排序,然后打倒出前50%中含有函数信息
 
    #如果想知道有哪些函数调用了bar,可使用
    p.print_callers(0.5, "bar")
 
    #同理,查看foo()函数中调用了哪些函数
    p.print_callees("foo")
