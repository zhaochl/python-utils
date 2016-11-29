#!/usr/bin/python
# -*- coding: utf-8 -*-

import email
import mimetypes
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import smtplib
from time import sleep
def sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText):

    strFrom = fromAdd
    strTo = ', '.join(toAdd)

    server = authInfo.get('server')
    user = authInfo.get('user')
    passwd = authInfo.get('password')

    if not (server and user and passwd) :
            print 'incomplete login info, exit now'
            return

    # 设定root信息
    msgRoot = MIMEMultipart('related')
    msgRoot['Subject'] = subject
    msgRoot['From'] = strFrom
    msgRoot['To'] = strTo
    msgRoot.preamble = 'This is a multi-part message in MIME format.'

    # Encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    #设定纯文本信息
    #msgText = MIMEText(plainText, 'plain', 'GB18030')
    msgText = MIMEText(plainText, 'plain', 'utf-8')
    msgAlternative.attach(msgText)

    #设定HTML信息
    #msgText = MIMEText(htmlText, 'html', 'GB18030')
    msgText = MIMEText(htmlText, 'html', 'utf-8')
    msgAlternative.attach(msgText)

    #设定内置图片信息
    #fp = open('test.jpg', 'rb')
    #msgImage = MIMEImage(fp.read())
    #fp.close()
    #msgImage.add_header('Content-ID', '<image1>')
    #msgRoot.attach(msgImage)

    #发送邮件
    smtp = smtplib.SMTP()
    #设定调试级别，依情况而定
    # 1-open log-
    #smtp.set_debuglevel(1)
    # 0-close log
    smtp.set_debuglevel(0)
    smtp.connect(server)
    smtp.login(user, passwd)
    smtp.sendmail(strFrom, strTo, msgRoot.as_string())
    smtp.quit()
    return

def sendmail(_title,_content,_toUserList,_html=None):
    #(authInfo, fromAdd, toAdd, subject, plainText, htmlText):
    print "start to send mail start"
    authInfo = {}
    authInfo['server'] = 'smtp.exmail.qq.com'
    authInfo['user'] = 'm@localhost.com'
    authInfo['password'] = '_R4VtnGslKnkvQAZTTr'
    fromAdd = 'm@localhost.com'
    #toAdd = ["root@localhost.com","houjianyu@localhost.com","t@localhost.com","biplus@localhost.com"]
    #toAdd = ["root@localhost.com","houjianyu@localhost.com","t@localhost.com","biplus@localhost.com"]
    #toAdd = ["root@localhost.com"]
    subject = 'search exception  category'
    if(_title):
        subject =_title

    plainText = _content
    #plainText = '服务器异常状态报警'

    htmlText = _html
    for t in _toUserList:
        #print t
        tarr=[]
        tarr.append(t)
        sendEmail(authInfo, fromAdd, tarr, subject, plainText, htmlText)
        sleep(2)
    print 'send mail success.'

"""
by zcl at 2016.6.15
"""
def rendar_table(title,notice,rhead_list,rdata_list):
    
    html ="""
    <p class="section">{0}</p>
    <p class="section">{1}</p>
    <table cellpadding="5" cellspacing="0" border="1" bordercolor="#04B4AE" style="text-align: center; font-family: Arial; border-collapse: collapse; width: auto;">
    <tbody>
        <tr>
            <td colspan="{2}"><div>{0}</div></td>
        </tr>
        <tr>
    """.format(title,notice,str(len(rhead_list)))
    for rhead in rhead_list:
        rhead = rhead.encode('utf8')
        tmp = """<th style="background-color: #04B4AE; color: #ffffff">{0}</th>
        """.format(str(rhead))
        html+=tmp
    html+="</tr>"

    for o in rdata_list:
        line_html=''
        line_html+="<tr>"
        for key in rhead_list:
            val = o[key]
            key = key.encode('utf8')
            line_html+="<td>"+str(val)+"</td>"
        line_html+="</tr>"
        html+=line_html
    html+="""
        </tbody>
        </table>
        <hr>
        """
    return html

if __name__ == '__main__' :
    toUserList = ['root@localhost.com']
    sendmail('test','sorry to disturb, this mail is just for test',toUserList)
    #sendmail('[热门行业统计]'+title,'',toUserList,html.encode('utf8'))
    #sendEmail(authInfo, fromAdd, toAdd, subject, plainText, htmlText)



