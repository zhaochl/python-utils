#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Zabbix SMTP Alert script from QQ.
"""
import sys
import smtplib
from email.mime.text import MIMEText

#邮件发送列表，发给哪些人
#mailto_list=["test1@test.com","test2@test.com"]
#设置服务器，用户名、口令以及邮箱的后缀
mail_host="smtp.exmail.qq.com"
user="test"
mail_user="test@test.com"
mail_pass="test"
mail_postfix="test.com"

#定义send_mail函数
def send_mail(to_list,sub,content):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("test@test.com","sub","content")
    '''
    address=user+"<"+user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject'] = sub
    msg['From'] = address
    msg['To'] =to_list
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user,mail_pass)
        s.sendmail(address, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
        send_mail(sys.argv[1], sys.argv[2], sys.argv[3])