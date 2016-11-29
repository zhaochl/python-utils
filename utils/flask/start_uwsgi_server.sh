#!/bin/bash
uwsgi -d _uwsgi.log --ini uwsgi.ini
ps -elf|grep uwsgi
echo 'start uwsgi server success'
