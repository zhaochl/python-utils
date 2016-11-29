#!/usr/bin/env python
# coding=utf-8
#pip install pypinyin
from pypinyin import pinyin, lazy_pinyin
import pypinyin


if __name__=="__main__":
    t=pinyin(u'中心')
    #[[u'zh\u014dng'], [u'x\u012bn']]
    print t
    for pinyin_list in t :
        for p in pinyin_list:
            print p.encode('utf8')
    t=pinyin(u'中心', heteronym=True)  # 启用多音字模式
    #[[u'zh\u014dng', u'zh\xf2ng'], [u'x\u012bn']]
    print t
    t=pinyin(u'中心', style=pypinyin.FIRST_LETTER)  # 设置拼音风格
    #[['z'], ['x']]
    print t

    t=pinyin(u'中心', style=pypinyin.TONE2, heteronym=True)
    #[['zho1ng', 'zho4ng'], ['xi1n']]
    print t
    
    t=lazy_pinyin(u'中心')  # 不考虑多音字的情况
    #['zhong', 'xin']
    print t
