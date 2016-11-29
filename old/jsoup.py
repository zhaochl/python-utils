#coding: utf-8
import sys
import urllib
import urllib2
from BeautifulSoup import BeautifulSoup
 
question_word = "吃货 程序员"
url = "http://www.baidu.com/s?wd=" + urllib.quote(question_word.decode(sys.stdin.encoding).encode('gbk'))
htmlpage = urllib2.urlopen(url).read()
soup = BeautifulSoup(htmlpage)
print len(soup.findAll("table", {"class": "result"}))
for result_table in soup.findAll("table", {"class": "result"}):
    a_click = result_table.find("a")
    print "-----标题----\n" + a_click.renderContents()#标题
    print "----链接----\n" + str(a_click.get("href"))#链接
    print "----描述----\n" + result_table.find("div", {"class": "c-abstract"}).renderContents()#描述
    print
