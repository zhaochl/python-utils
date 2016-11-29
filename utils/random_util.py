#!/usr/bin/env python
# coding=utf-8
import random

"""
>>> import random
>>> random.randint(0,99)
21

随机选取0到100间的偶数：
>>> import random
>>> random.randrange(0, 101, 2)
42

随机浮点数：
>>> import random
>>> random.random()
0.85415370477785668
>>> random.uniform(1, 10)
5.4221167969800881

随机字符：
>>> import random
>>> random.choice('abcdefg&#%^*f')
'd'

多个字符中选取特定数量的字符：
>>> import random
random.sample('abcdefghij',3)
['a', 'd', 'b']

多个字符中选取特定数量的字符组成新字符串：
>>> import random
>>> import string
>>> string.join(random.sample(['a','b','c','d','e','f','g','h','i','j'], 3)).r
eplace(" ","")
'fih'

随机选取字符串：
>>> import random
>>> random.choice ( ['apple', 'pear', 'peach', 'orange', 'lemon'] )
'lemon'

洗牌：
>>> import random
>>> items = [1, 2, 3, 4, 5, 6]
>>> random.shuffle(items)
>>> items
[3, 2, 5, 6, 4, 1]

"""
def random_str(randomlength=32):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789~`!@#$%^&*()_+-=,./<>?;:[]{}\|'
    length = len(chars) - 1
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
t=random_str()
print t
t= random.randint(0,99)
print t
