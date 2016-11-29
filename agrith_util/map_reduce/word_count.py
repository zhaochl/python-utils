#!/usr/bin/env python
# coding=utf-8
from map_reduce import *
import re
#http://www.cnblogs.com/rubinorth/p/5780531.html
class WordCount:
    __doc__ = '''词频统计'''

    def mapper(self, input_key, input_value):
        """
        词频统计的mapper方法
        :param input_key: 文件名
        :param input_value: 文本内容
        :return: 以(词,1)为元素的一个列表
        """
        return [(word, 1) for word in
                self.remove_punctuation(input_value.lower()).split()]

    def reducer(self, intermediate_key, intermediate_value_list):
        """
        词频统计的reducer方法
        :param intermediate_key: 某个词
        :param intermediate_value_list: 出现记录列表，如[1,1,1]
        :return: (词,词频)
        """
        return intermediate_key, sum(intermediate_value_list)

    @staticmethod
    def remove_punctuation(text):
        """
        去掉字符串中的标点符号
        :param text: 文本
        :return: 去掉标点的文本
        """
        return re.sub(u"\p{P}+", "", text)

if __name__=='__main__':
    filenames = ["text/a.txt", "text/b.txt", "text/c.txt"]
    i = {}
    for filename in filenames:
        f = open(filename)
    i[filename] = f.read()
    f.close()

    wc = WordCount()
    print(MapReduce.map_reduce(i, wc.mapper, wc.reducer))

