#!/bin/bash
yesterday=`date --date="now -1 day" +"%Y-%m-%d %H:%M:%S"`
weekbefore=`date --date="now -7 day" +"%Y-%m-%d %H:%M:%S"`
#`date --date="now" +"%Y-%m-%d %H:%M:%S"`
#echo 'yesterday is:'$yesterday
today=`date --date="now" +"%Y-%m-%d %H:%M:%S"`
#echo 'today is:'$today
result1=`python job_main.py "$yesterday" "$today" 20000`
result2=`python job_main.py "$weekbefore" "$today" 20000`
message=$yesterday,$today,$result1
echo $message >>job_result_daybefore.csv

message=$weekbefore,$today,$result2
echo $message >>job_result_weekbefore.csv
