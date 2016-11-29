#!/usr/bin/env python
# coding=utf-8
import os
import logging
import logging.handlers
from datetime import datetime
#datefmt='%a, %d %b %Y %H:%M:%S',
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                    #datefmt='%a, %d %b %Y %H:%M:%S',
                    filename = os.path.join(os.getcwd(),'app.log'),
                    filemode='a')

def p(info):
    _n= datetime.now()
    _today= _n.strftime("%Y-%m-%d %H:%M:%S")
    print _today+" "+info
def I(info):
    logging.info(info)
    p(info)
def D(info):
    logging.debug(info)
    p(info)
def W(info):
    logging.warning(info)
    p(info)
def E(info):
    logging.error(info)
    p(info)

if __name__=='__main__':
    print '-main-'
    I('info..')
    D('debug..')
    W('warn..')
    E('error..')
