#!/bin/bash
if  [  -d  _tmp_0 ];then
    echo  "exist"
    exit
else
    mkdir _tmp_0
fi
cp /path/xxx.pdf _tmp_0/
tar -zcvf _tmp_0.tar.gz _tmp_0

ftp -n <<- EOF
open localhost
user name password
cd /path/
bin
put _tmp_0.tar.gz
bye
EOF
    rm -rf _tmp_0.tar.gz
    rm -rf _tmp_0
echo 'run at' `date +'%Y/%m/%d %H:%M:%S'`,file:_tmp_0.tar.gz
