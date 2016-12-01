#!/usr/bin/env python
# coding=utf-8
from file_util import *
from pdb import *

import commands
import urllib2

#output = os.popen('ls')
#print output.read()

#print '----------------------------'
#(status, output) = commands.getstatusoutput('ls')
#print status, output
def execute_cmd(cmd):
    _result={}
    (status, output) = commands.getstatusoutput(cmd)
    _result['status'] = status
    _result['output'] = output
    return _result
def gen_ftp_sh(file_name):
    _content = """
ftp -n <<- EOF
open timeplan.cn
user name password
cd /path/
bin
put {}
bye
EOF
    """.format(file_name)
    return _content
def gen_test_dir(dir_name):
    _content="""
if  [  -d  {} ];then
    echo  "exist"
    exit
else
    mkdir {}
fi
    """.format(dir_name,dir_name)
    return _content
def main():
    name_list = read_file_line('list')
    content = '#!/bin/bash\n'
    content_file=''
    next_dir_index = 0
    for index,name in enumerate(name_list):
        if len(name)==1:
            continue
        name = name.encode('utf8','ignore')
        dir_name = '_tmp_'+str(next_dir_index)
        content_file +='cp /path/'+name +' '+dir_name+'/\n'
        tar_name = dir_name+'.tar.gz'
        if index%100==0:
            f_name = '_bash_/bash_'+str(index)+'.sh'
            
            #content+='mkdir '+dir_name+'\n'
            content+=gen_test_dir(dir_name)
            content+=content_file

            content+="tar -zcvf "+ tar_name+' '+dir_name+'\n'
            content+= gen_ftp_sh(tar_name)
            content+='rm -rf '+tar_name+'\n'
            content+='rm -rf '+dir_name+'\n'
            content +="echo 'run at' `date +'%Y/%m/%d %H:%M:%S'`,file:"+tar_name+'\n'
            content_file=''
            next_dir_index = (index+100)/100
            write_file(f_name,content)
            content = '#!/bin/bash\n'
            #if index>=2:
            #    break
    print 'ok'

if __name__=='__main__':
    #result = execute_cmd('ls')
    #print result['output']
    main()
