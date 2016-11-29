#!/bin/bash
logfile=results_job_main_all_work.txt
rm -rf $logfile
for (( i=6;i>=0;i-- ))
do
    echo '---------run start-----'>>$logfile
    #week1=`date --date="now -$i week" +"%Y-%m-%d %H:%M:%S"`
    #week2=`date --date="now -$(($i+1)) week" +"%Y-%m-%d %H:%M:%S"`
    week1=`date --date="now -0 week" +"%Y-%m-%d %H:%M:%S"`
    week2=`date --date="now -1 week" +"%Y-%m-%d %H:%M:%S"`
    echo '---date from '$week2' to '$week1' -------' >>$logfile
    python -u job_main.py "$week2" "$week1" 30000 $(($i*60*10)) >>$logfile
    echo '---------run end---------'>>$logfile
done
echo 'success'
