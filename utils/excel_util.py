#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
#pip install xlrd
#pip install xlwt
import xlrd
import xlwt
import sys
from datetime import date,datetime
import os
def read_excel(filename):
  
    workbook = xlrd.open_workbook(filename)
    # print sheet2.name,sheet2.nrows,sheet2.ncols
    sheet2 = workbook.sheet_by_index(0)

    f = file('tmp.csv','w')
    data_list =[]
    for row in xrange(0, sheet2.nrows):
        rows = sheet2.row_values(row)
        def _tostr(cell):
            if type(u'') == type(cell): 
                return "%s" % cell.encode('utf8')
            else:
                return "%s" % str(cell) 

        line_info = ','.join([_tostr(cell) for cell in rows ])
        if row==0:
            print line_info
            print len(line_info.split(','))
        data_list.append(line_info)
        f.write(line_info+'\n')
    f.close()
    return data_list
if __name__ == '__main__':
  filename = sys.argv[1]
  read_excel(filename)
