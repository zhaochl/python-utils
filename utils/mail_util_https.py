#!/usr/bin/env python
# coding=utf-8
#!/usr/bin/python
# -*- coding: utf-8 -*-
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate
import smtplib

MAIL_HOST = 'smtp.exmail.qq.com'
MAIL_USERNAME = "m@localhost.com"
MAIL_PASSWORD = "123456"

def Letter(subject, content, From, To):
    if isinstance(To, basestring):
        To = [To]
    mail = MIMEText(
        content,
        _subtype="html",
        _charset="utf-8"
    )
    mail['Subject'] = Header(subject, 'utf-8')
    mail['From'] = From
    mail['To'] = ';'.join(To)
    mail['Date'] = formatdate()

    return mail.as_string()
def send_email(email_addresses, subject, content):
    letter = Letter(subject, content, MAIL_USERNAME, email_addresses)
    try:
        smtp = smtplib.SMTP_SSL(MAIL_HOST, smtplib.SMTP_SSL_PORT)
        smtp.login(MAIL_USERNAME, MAIL_PASSWORD)

        smtp.sendmail(MAIL_USERNAME, email_addresses, letter)
        smtp.close()
        print "Successfully to send mails"
    except Exception as e:
        print e
#sendmail('[monitor](APP)search search service available exception','',toUserList,except_mail_info)
def sendmail(title,content,toUserList,_html=None):
    for user in toUserList:
        title = '[VPC]'+title
        send_email(user,title,_html)

if __name__=='__main__':
    send_email('root@localhost.com', 'subject', 'content')
    print 'ok'
    title='test'
    content='aaa'
    toUserList = ['root@localhost.com']
    sendmail(title,content,toUserList)
