#!/bin/bash
if [ `whoami` != "root" ];then
        echo "Run this tool needs root user."
        exit 1
fi
 
nscd -i hosts
service nscd restart
yum -y install epel-release
yum -y install nginx
yum -y install python-pip
yum -y install python-gevent
yum -y install python-setuptools
yum -y install supervisor
#yum -y install uwsgi
yum -y install redis
yum install libxml2
yum install libxml2-devel -y
pip install redis
yum install graphviz-dev graphviz
pip install graphviz
yum -y install python-devel
yum -y install mysql-devel
#uwsgi
pip install uwsgi
yum -y install uwsgi-plugin-python
yum -yinstall libxml*
pip -y install MySQL-python==1.2.3
pip install django==1.8.3
pip install numpy
#pip install matplotlib
pip install pycrypto==2.6.1
pip install html5lib
pip install beautifulsoup4
pip install lxml
pip install peewee
pip install pypinyin
pip install pinyin
echo 'install ok'
