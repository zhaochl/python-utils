#!/bin/bash
kill -9 `ps -elf|grep uwsgi|awk '{print $4}'|head -n1`
ps -elf|grep uwsgi
echo 'shut ok'
