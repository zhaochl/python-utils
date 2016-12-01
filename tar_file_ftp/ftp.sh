#!/bin/bash
FTILE_NAME=$1
ftp -n <<- EOF
open localhost
user name passwd
cd /path/
bin
put $FTILE_NAME
bye
EOF
