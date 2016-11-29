#!/usr/bin/env python
# coding=utf-8
from random import choice
import string
def Makepass(length=8, chars=string.letters+string.digits):
    return ''.join([choice(chars) for i in range(length)])

if __name__ == '__main__':
    for i in range(20):
        print Makepass(16)
