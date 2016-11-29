#!/usr/bin/env python
# coding=utf-8

# -*- coding: utf-8 -*-
import urllib2

import re
import string
import operator

#剔除常用字函数
def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have",
                   "it", "i", "that", "for", "you", "he", "with", "on", "do", "say",
                   "this", "they", "is", "an", "at", "but","we", "his", "from", "that",
                   "not", "by", "she", "or", "as", "what", "go", "their","can", "who",
                   "get", "if", "would", "her", "all", "my", "make", "about", "know",
                   "will","as", "up", "one", "time", "has", "been", "there", "year", "so",
                   "think", "when", "which", "them", "some", "me", "people", "take", "out",
                   "into", "just", "see", "him", "your", "come", "could", "now", "than",
                   "like", "other", "how", "then", "its", "our", "two", "more", "these",
                   "want", "way", "look", "first", "also", "new", "because", "day", "more",
                   "use", "no", "man", "find", "here", "thing", "give", "many", "well"]

    if ngram in commonWords:
        return True
    else:
        return False

def cleanText(input):
    input = re.sub('\n+', " ", input).lower() # 匹配换行用空格替换成空格
    input = re.sub('\[[0-9]*\]', "", input) # 剔除类似[1]这样的引用标记
    input = re.sub(' +', " ", input) #  把连续多个空格替换成一个空格
    input = bytes(input)#.encode('utf-8') # 把内容转换成utf-8格式以消除转义字符
    #input = input.decode("ascii", "ignore")
    return input

def cleanInput(input):
    input = cleanText(input)
    cleanInput = []
    input = input.split(' ') #以空格为分隔符，返回列表


    for item in input:
        item = item.strip(string.punctuation) # string.punctuation获取所有标点符号

        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'): #找出单词，包括i,a等单个单词
            cleanInput.append(item)
    return cleanInput

def getNgrams(input, n):
    input = cleanInput(input)

    output = {} # 构造字典
    for i in range(len(input)-n+1):
        ngramTemp = " ".join(input[i:i+n])#.encode('utf-8')

        if isCommon(ngramTemp.split()[0]) or isCommon(ngramTemp.split()[1]):
            pass
        else:
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

#方法一：对网页直接进行读取
content = urllib2.urlopen(urllib2.Request("http://pythonscraping.com/files/inaugurationSpeech.txt")).read()
#对本地文件的读取，测试时候用，因为无需联网
#content = open("1.txt").read()
ngrams = getNgrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True)[0:5] # reverse=True 降序排列
print(sortedNGrams)
for top3 in range(3):
    print "###"+getFirstSentenceContaining(sortedNGrams[top3][0],content.lower())+"###"
