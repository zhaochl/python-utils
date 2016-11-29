#!/usr/bin/env python
# coding=utf-8
import jieba
import jieba.posseg as pseg
jieba.initialize()

#全模式
text = "我来到北京清华大学"
seg_list = jieba.cut(text, cut_all=True)
print u"[全模式]: ", "/ ".join(seg_list) 

#精确模式
seg_list = jieba.cut(text, cut_all=False)
print u"[精确模式]: ", "/ ".join(seg_list)

#默认是精确模式
seg_list = jieba.cut(text)
print u"[默认模式]: ", "/ ".join(seg_list) 

#新词识别 “杭研”并没有在词典中,但是也被Viterbi算法识别出来了
seg_list = jieba.cut("他来到了网易杭研大厦") 
print u"[新词识别]: ", "/ ".join(seg_list)

#搜索引擎模式
seg_list = jieba.cut_for_search(text) 
print u"[搜索引擎模式]: ", "/ ".join(seg_list)


print "\n========"
test_sent = "李小福是创新办主任也是云计算方面的专家;"
print 'origin sentence:',test_sent
print '--before userdict seg result:---'
words = jieba.cut(test_sent)
for w in words:
    print w
print '--after userdict seg result:---'
jieba.load_userdict('mydict.dict')

words = jieba.cut(test_sent)
for w in words:
    print w
result = pseg.cut(test_sent)

for w in result:
    print w.word, "/", w.flag, ", ",

print "\n========"
print '---jieba keyword extract--'
import jieba.analyse
topK=5
keywords = jieba.analyse.extract_tags(test_sent,topK)
for keyword in keywords:
    print keyword
