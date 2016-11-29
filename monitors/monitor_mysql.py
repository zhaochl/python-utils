#!/usr/bin/env python
# coding=utf-8
from shell_util import *
def check_main(procss):
    
    _result = None
    status,output = run_cmd('nc -vv localhost 3306')
    #print status
    #print output
    if 'succeeded' in output:
        print procss+' run success!'
        _result = 'ok'
    else:
        print procss+' run error!'
        run_cmd('/etc/init.d/mysqld start')
        _result ='error,and restarted.'
    return _result

if __name__=='__main__':
    print ' monitor jobs'
    check_main('mysql')
