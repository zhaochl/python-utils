#!/bin/bash

echo $RANDOM
#$RANDOM 的范围是 [0, 32767]

function rand(){
    min=$1
    max=$(($2-$min+1))
    num=$(date +%s%N)
    #echo $(($num%$max+$min))
}

echo '-------'
rnd=$(rand 1 50)
echo $rnd

echo '-------'
#使用date 生成随机字符串
date +%s%N | md5sum | head -c 10

echo '-------\n'
#使用 /dev/urandom 生成随机字符串
cat /dev/urandom | head -n 10 | md5sum | head -c 10


exit 0
