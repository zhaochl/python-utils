#!/usr/bin/env python
# coding=utf-8
import re 
def regex_replace(reg_str,src_str,to_str):
    find_str = re.sub(r""+reg_str+"",to_str,src_str)
    return find_str
def regex_search_all(reg_str,src_str):
    result_arr = []
    pattern = re.compile(reg_str)
    result_arr = pattern.findall(src_str)
    return result_arr

def regex_search(reg_str,src_str):
    results = None
    #src_str = src_str.strip().strip('\n')
    #src_str = src_str.replace(' ','')
    #print 'src_str:',src_str
    match_obj = re.search( r""+reg_str+"", src_str, re.M|re.I )
    if match_obj:
        results = match_obj.group()
    return results
def regex_help():
    s=\
    """
    re.l    使匹配对大小写不敏感
    re.L    做本地化识别（locale-aware）匹配
    re.M    多行匹配，影响 ^ 和 $
    re.S    使 . 匹配包括换行在内的所有字符
    re.U    根据Unicode字符集解析字符。这个标志影响 \w, \W, \b, \B.
    re.X    该标志通过给予你更灵活的格式以便你将正则表达式写得更易于理解。e
    """
    print s
def demo():
    #-----------replace----------
    phone = "2004-959-559 # This is Phone Number"
    # Delete Python-style comments
    num = re.sub(r'#.*$', "", phone)
    print "Phone Num : ", num

    # Remove anything other than digits
    num = re.sub(r'\D', "", phone)    
    print "Phone Num : ", num

    #-------search ----
    # match find from first,search from all
    #http://www.runoob.com/python/python-reg-expressions.html
    line = "Cats are smarter than dogs";
    matchObj = re.match( r'dogs', line, re.M|re.I)
    if matchObj:
       print "match --> matchObj.group() : ", matchObj.group()
    else:
       print "No match!!"

    matchObj = re.search( r'dogs', line, re.M|re.I)
    if matchObj:
       print "search --> matchObj.group() : ", matchObj.group()
    else:
       print "No match!!"


def is_alphabet(title):
    _result = False
    arr = re.findall(r"[a-zA-Z]+",title)
    
    if arr!=None and len(arr)>0:
        str = arr[0]
        if len(str)==len(title):
            _result = True
    return _result

if __name__=='__main__':
    #demo()
    """
    s = "Cats are smarter than dogs";
    reg = 'dogs'
    r = regex_search(reg,s)
    print r,type(r)
    
    #---把数字替换成'数字'
    s = "2004-959-559 # This is Phone Number"
    reg='\d'
    r =  regex_replace(reg,s,'数字')
    print r
    regex_help()
    #reg='20\d{2}-\d+-\d+\s\d{2}:\d{2}:\d{2}'
    reg='20\d{2}\s+年\s+\d+\s+月\s+\d{2}\s+日'
    #str='I have a meeting at 2013-4-2 08:30:11'
    str='2016 年 5 月 24 日 云湛作者：云湛'
    t= regex_search(reg,str)
    print t
    str="(7,0.75) (17,0.25)"
    #str='(7,1)'
    reg="(\d+,0.\d+)+"
    t= regex_search_all(reg,str)
    print t
    
    str='(7,1)'
    reg="(\d+,1)+"
    pattern = re.compile(reg)
    result_arr = pattern.findall(str)
    print result_arr
    str='xx2015.04.13ss'
    reg="\d+\.\d+\.\d+"
    t= regex_search_all(reg,str)
    print t
    s = 'aBstsdfa'
    t= is_alphabet(s)
    print t   
    """
    reg = '((人|项目).*靠谱)+'
    #s='人不怎么靠谱assss,人很靠谱xxxsws'
    s='项目挺好，但人不靠谱xxxss'
    #t= regex_search(reg,s)
    #print t
    t=regex_replace(reg,s,'<em>'+s+'</em>')
    print t


