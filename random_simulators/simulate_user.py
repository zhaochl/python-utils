#!/usr/bin/env python
# coding=utf-8
from constant import *
from random import *
from simulate_util import *
from pdb import *
def rd_cn_name():
    _name =''
    xing_index = randint(0,98)
    #print xing_index
    xing = CONST_XING[xing_index]
    #print xing
    _name = xing
    for i in range(randint(1,2)):
        ming = random_chinese_str()
        _name+=ming
    return _name

def gen_name():
    name=''
    x = randint(0,98)
    xing = CONST_XING[x]
    ming_list = CONST_MING_MAN+CONST_MING_WOMEN
    m = randint(0,len(ming_list)-1)
    ming = ming_list[m]
    name+=xing+ming
    return name

def rd_en_name(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789_'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
def rd_user_action():
    todo_len = len(CONST_ACTION_LIST)
    action_index = randint(0,todo_len-1)
    return CONST_ACTION_LIST[action_index]
if __name__=='__main__':
    #print 'main'
    num=5
    for i in range(num):
        #cn_name= rd_cn_name()
        cn_name= gen_name()
        en_name = rd_en_name()
        action = rd_user_action()
        r = cn_name+","+"("+en_name+")"+action
        print r
