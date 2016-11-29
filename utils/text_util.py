#!/usr/bin/env python
# coding=utf-8

"""汉字处理的工具:
判断unicode是否是汉字，数字，英文，或者其他字符。
全角符号转半角符号。"""
 
"""判断一个unicode是否是汉字"""
def is_chinese(uchar):
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False
 
"""判断一个unicode是否是数字"""
def is_number(uchar):
        if uchar >= u'\u0030' and uchar<=u'\u0039':
                return True
        else:
                return False
 
"""判断一个unicode是否是英文字母"""
def is_alphabet(uchar):
        if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
                return True
        else:
                return False
 
"""判断是否非汉字，数字和英文字符"""
def is_other(uchar):
        if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):
                return True
        else:
                return False
"""判断是否含有汉字，数字，英文字符以外的字符"""
def has_abnormal_char(str):
    result =False
    b=unicode(str)
    for r in b:
        t = is_other(r)
        r = r.encode('utf8')
        if t:
            result=True
            break
    return result
"""半角转全角"""
def B2Q(uchar):
        inside_code=ord(uchar)
        if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
                return uchar
        if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
                inside_code=0x3000
        else:
                inside_code+=0xfee0
        return unichr(inside_code)
 
"""全角转半角"""
def Q2B(uchar):
        inside_code=ord(uchar)
        if inside_code==0x3000:
                inside_code=0x0020
        else:
                inside_code-=0xfee0
        if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
                return uchar
        return unichr(inside_code)
 
"""把字符串全角转半角"""
def stringQ2B(ustring):
        return "".join([Q2B(uchar) for uchar in ustring])
 
"""格式化字符串，完成全角转半角，大写转小写的工作"""
def uniform(ustring):
        return stringQ2B(ustring).lower()
 
"""将ustring按照中文，字母，数字分开"""
def string2List(ustring):
        retList=[]
        utmp=[]
        for uchar in ustring:
                if is_other(uchar):
                        if len(utmp)==0:
                                continue
                        else:
                                retList.append("".join(utmp))
                                utmp=[]
                else:
                        utmp.append(uchar)
        if len(utmp)!=0:
                retList.append("".join(utmp))
        return retList
def is_chinese_str(_str):
    str  = unicode(_str)
    result = False
    is_chinese_count=0
    for r in str:
        if is_chinese(r):
            is_chinese_count+=1
    if is_chinese_count==len(str):
        result = True
    return result
def test():
    s='a'
    print len(s)
    #1
    s='ab'
    print len(s)
    #2
    s='一'
    print len(s)
    #3
def test_ascii():
    char ='A'
    # Get the ASCII number of a character
    number = ord(char)
    print 'A ASCII->',number
    # Get the character given by an ASCII number
    char = chr(number)
    print number,'->char:',char
    #ord 必须是unicode
    print '我->ASCII:',ord(u'我'),',str:',unichr(ord(u'我'))
if __name__=="__main__":
        """
        #test Q2B and B2Q
        for i in range(0x0020,0x007F):
                print Q2B(B2Q(unichr(i))),B2Q(unichr(i))
 
        #test uniform
        ustring=u'中国 人名ａ高频Ａ'
        ustring=uniform(ustring)
        ret=string2List(ustring)
        print ret
        """
        #a='abc123中国s-@'
        #t = has_abnormal_char(a)
        #print t
        t='0a11'
        a=is_number(t)
        print a
        s='中123'
        print len(s),len(unicode(s))
        s='科技'
        print is_chinese_str(s)
        #test()
        test_ascii()
