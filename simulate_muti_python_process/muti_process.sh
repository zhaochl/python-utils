#!/bin/bash
if (($#<2))
then
    echo "usage:"
    echo "./yali.sh number_of_proc program_name"
    exit
fi

prog_name=$2" "$3
num_proc=$1
pid_file="/tmp/pid.yali"

>$pid_file

trap "cat $pid_file | xargs kill -9 " EXIT

for ((i=0;i<$num_proc;i++))
do
    echo $prog_name
    $prog_name 2>&1 &
    echo $! >> $pid_file
done

wait
