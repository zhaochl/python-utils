#!/bin/bash
yesterday=`date --date="now -1 day" +"%Y-%m-%d %H:%M:%S"`
#`date --date="now" +"%Y-%m-%d %H:%M:%S"`
echo 'yesterday is:'$yesterday
today=`date --date="now" +"%Y-%m-%d %H:%M:%S"`
echo 'today is:'$today
python job_main.py "$yesterday" "$today" 100
