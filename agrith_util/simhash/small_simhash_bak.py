#!/usr/bin/env python
# coding=utf-8
import jieba
import jieba.posseg as pseg
jieba.tmp_dir ='./tmp/'
jieba.cache_file='./tmp/jieba.cache'
jieba.initialize()

word_weight = {
    '美国':4,
    '51区':5,
    '雇员':3, 
    '称':1,
    '内部':2, 
    '有':1,
    '9架':3,
    '飞碟':5,
    '曾':1,
    '看见':3,
    '灰色':4,
    '外星人':5
}

def calc_sim_hash(text):
    seg_list = jieba.cut(text,cut_all=True)
    for w in seg_list:
        w = str(w)
        if word_weight.has_key(w):
            print word_weight[w]

if __name__=='__main__':
    print word_weight
    text = '美国“51区”雇员称内部有9架飞碟，曾看见灰色外星人'
    #sentence1='美国“51区”雇员称内部有9架飞碟，曾看见灰色外星人'
    #simhash1 = calc_sim_hash(text)
    seg_list = jieba.cut(text)
    for r in seg_list:
        print r
