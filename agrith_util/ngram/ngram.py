#!/usr/bin/env python
# coding=utf-8

# -*- coding: utf-8 -*-
import urllib2

import re
import string
import operator

#剔除常用字函数
commonWords = ["the", "be", "and", "of", "a", "in", "to", "have",\
               "it", "i", "that", "for", "you", "he", "with", "on", "do", "say",\
                   "this", "they", "is", "an", "at", "but","we", "his", "from", "that",\
                   "not", "by", "she", "or", "as", "what", "go", "their","can", "who",\
                   "get", "if", "would", "her", "all", "my", "make", "about", "know",\
                   "will","as", "up", "one", "time", "has", "been", "there", "year", "so",\
                   "think", "when", "which", "them", "some", "me", "people", "take", "out",\
                   "into", "just", "see", "him", "your", "come", "could", "now", "than",\
                   "like", "other", "how", "then", "its", "our", "two", "more", "these",\
                   "want", "way", "look", "first", "also", "new", "because", "day", "more",\
                   "use", "no", "man", "find", "here", "thing", "give", "many", "well"]

def init_common_dict():
    d = {}
    for w in commonWords:
        d[w] = 1
    return d


def cleanText(input):
    input = re.sub('\n+', ".", input).lower() # 匹配换行用空格替换成空格
    input = re.sub('\[[0-9]*\]', "", input) # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    input = bytes(input)#.encode('utf-8') # 把内容转换成utf-8格式以消除转义字符
    #input = input.decode("ascii", "ignore")
    return input

def str_to_sentence_list(content_str):
    sentence_list = []
    sign_list = ['.',',',':','，','。']
    sentence=''
    for r in unicode(content_str):
        if not r in sign_list:
            sentence+=r
        else:
            if sentence.strip(' ')!='':
                sentence_list.append(str(sentence))
                sentence=''
    return sentence_list

        
def tmp():
    def DFS(content_str,queue):
        queue.append(content_str)
        while len(queue)>0:
            sub_sentence = queue.pop()
            null_sign_count =0
            for sign in sign_list:
                if sub_sentence.find(sign)!=-1:
                    sub_sentence_list = sub_sentence.split(sign)
                    for sub_sentence_t in sub_sentence_list:
                        queue.append(sub_sentence_t)
                else:
                    null_sign_count+=1
                    if null_sign_count==len(sign_list):
                        visited[sub_sentence] =1
                        sentence_list.append(sub_sentence)
    queue =[]
    visited = {}
    queue.append(content_str)
    DFS(content_str)
    print visited
    print sentence_list

def sentence_to_word_list(sentence_str,use_common_word=True):
    common_word_dict = init_common_dict()
    word_list = []
    word_content_list = sentence_str.split(' ') #以空格为分隔符，返回列表


    for item in word_content_list:
        #item = item.strip(string.punctuation) # string.punctuation获取所有标点符号
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'): #找出单词，包括i,a等单个单词
            if not use_common_word:
                if not common_word_dict.has_key(item):
                    word_list.append(item)
            else:
                word_list.append(item)

    return word_list

def getNgram(sentence, n):
    
    output = {} # 构造字典
    for i in range(len(sentence)-n+1):
        ngram_list = sentence[i:i+n]
        ngramTemp = " ".join(ngram_list)#.encode('utf-8')
        
        if ngramTemp not in output: #词频统计
            output[ngramTemp] = 0 #典型的字典操作
        output[ngramTemp] += 1
    return output

#获取核心词在的句子
def getFirstSentenceContaining(ngram, content):
    #print(ngram)
    sentences = content.split(".")
    for sentence in sentences:
        if ngram in sentence:
            return sentence
    return ""

def ngram_main():
    #方法一：对网页直接进行读取
    #content = urllib2.urlopen(urllib2.Request("http://pythonscraping.com/files/inaugurationSpeech.txt")).read()
    #对本地文件的读取，测试时候用，因为无需联网
    content = open("inaugurationSpeech.txt").read()
    content = cleanText(content)
    sentence_list = str_to_sentence_list(content)
    word_sentence_rindex = {}
    for index,sentence in enumerate(sentence_list):
        word_list = sentence_to_word_list(sentence)
        for word in word_list:
            if not word_sentence_rindex.has_key(word):
                word_sentence_rindex[word] = [index]
            else:
                word_sentence_rindex[word] += [index]
    
    all_word_list = []
    all_word_list = word_sentence_rindex.keys()
    ngram = getNgram(all_word_list, 3)
    sorted_ngram = sorted(ngram.items(), key = operator.itemgetter(1), reverse=True)[0:3] # reverse=True 降序排列
    print(sorted_ngram)
    for top3 in range(3):
        print "###"+getFirstSentenceContaining(sorted_ngram[top3][0],content.lower())+"###"

def test_str_to_sentence():
    content ='aa,11 22,ss ee.oo,pp'
    t = str_to_sentence_list(content)
    print t
if __name__=='__main__':
    ngram_main()
