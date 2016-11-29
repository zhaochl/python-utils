#!/bin/bash

#killall python
#pid=ps -ef |grep `netstat -lnp |grep LISTEN|grep 1862|awk -F[/] '{print $NF}'`|awk '{print $2}'
#pid="ps -aux|netstat -naltp | grep :1862 | awk '{print $7}' | awk -F"/" '{ print $1 }'"
#echo $pid

#killall nginx


pid=$(/usr/sbin/lsof -i:1872 -t); kill -TERM $pid || kill -KILL $pid
echo $pid

echo 'django killed'
