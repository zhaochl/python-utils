#!/bin/bash
PARA_CNT=$#
TRASH_DIR="/home/chunliang/.trash"
for i in $*; do
     STAMP=`date +'%Y-%m-%d'`
     fileName=`basename $i`
     mv $i $TRASH_DIR/$fileName.$STAMP
done
