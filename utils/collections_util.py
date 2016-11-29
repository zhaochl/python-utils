#!/usr/bin/env python
# coding=utf-8
from collections import *
import sys
import time
"""
collections模块基本介绍
我们都知道，Python拥有一些内置的数据类型，比如str, int, list, tuple, dict等， collections模块在这些内置数据类型的基础上，提供了几个额外的数据类型：
1.namedtuple(): 生成可以使用名字来访问元素内容的tuple子类
2.deque: 双端队列，可以快速的从另外一侧追加和推出对象
3.Counter: 计数器，主要用来计数
4.OrderedDict: 有序字典
5.defaultdict: 带有默认值的字典
"""

"""
namedtuple主要用来产生可以使用名称来访问元素的数据对象，通常用来增强代码的可读性， 在访问一些tuple类型的数据时尤其好用
"""
def test_namedtuple():
    websites = [
            ('Sohu', 'http://www.google.com/', u'张朝阳'),
            ('Sina', 'http://www.sina.com.cn/', u'王志东'),
            ('163', 'http://www.163.com/', u'丁磊')

    ]
    Website = namedtuple('Websites', ['name', 'url', 'founder'])
    for website in websites:
        website = Website._make(website)
        print website,website.name
"""
deque其实是 double-ended queue 的缩写，翻译过来就是双端队列，它最大的好处就是实现了从队列 头部快速增加和取出对象: .popleft(), .appendleft() 
"""
def test_horse_light():
    fancy_loading = deque('>--------------------')
    while True:
        print '\r%s' % ''.join(fancy_loading),
        fancy_loading.rotate(1)
        sys.stdout.flush()
        time.sleep(0.08)
    # Result:
    # 一个无尽循环的跑马灯   
def test_deque():
    msg = deque('abcdefg')
    msg.popleft()
    msg.appendleft('h')
    print msg
    msg.rotate()
    print msg
def test_counter():
    s = '''A Counter is a dict subclass for counting hashable objects. It is an unordered collection where elements are stored as dictionary keys and their counts are stored as dictionary values. Counts are allowed to be any integer value including zero or negative counts. The Counter class is similar to bags or multisets in other languages.'''.lower()
    c = Counter(s)
    # 获取出现频率最高的5个字符
    print c.most_common(5)
"""
在Python中，dict这个数据结构由于hash的特性，是无序的,orderdict 是有序的dict
"""
def test_orderdict():
    items = (
        ('A', 1),
        ('B', 2),
        ('C', 3)
    )
    regular_dict = dict(items)
    ordered_dict = OrderedDict(items)
    print 'Regular Dict:'
    for k, v in regular_dict.items():
        print k, v
    print 'Ordered Dict:'
    for k, v in ordered_dict.items():
        print k, v
"""
在使用Python原生的数据结构dict的时候，如果用 d[key] 这样的方式访问， 当指定的key不存在时，是会抛出KeyError异常的。
但是，如果使用defaultdict，只要你传入一个默认的工厂方法，那么请求一个不存在的key时， 便会调用这个工厂方法使用其结果来作为这个key的默认值
"""
def test_defaultdict():
    dict_set1 = {}  
    #如果不知道这个字段中key有没有，需要先判断  
    if 'key' not in dict_set1:  
        dict_set1['key'] = set()  
    dict_set1['key'].add('111')  
    dict_set1['key'].add('000')  
    print dict_set1  
    dict_set = defaultdict(set)  
    dict_set['key'].add('000')  
    dict_set['key'].add('111')  
    print dict_set
    ss = '1111222233334444'  
    dict_int = defaultdict(int)  
    for s in ss:  
        dict_int[s] += 1  
    print dict_int 
    #带有统计性质的数据操作时很好用
    s = [('yellow', 1), ('blue', 2), ('yellow', 3), ('blue', 4), ('red', 1)] 
    d = defaultdict(list) 
    for k, v in s: 
        d[k].append(v)
    print d.items()
    print d
if __name__=='__main__':
    #test_namedtuple()
    #test_deque()
    #test_counter()
    #test_orderdict()
    test_defaultdict()
