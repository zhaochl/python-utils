#!/usr/bin/env python
# coding=utf-8
from data_util import *


def get_tb_mapper(tb):
    fields = {}
    sql="desc "+tb;
    results = DataUtil.db_query('online','mydb',sql);
    #print results
    for field in results:
        fieldname = field[0].encode('utf8','ignore')
        typename = field[1].encode('utf8','ignore')
        fields[fieldname] = typename
    print fields
    return fields
def get_tb_all_fields_sql(tb,limit=None):
    
    fields = get_tb_mapper(tb)
    fields_names = fields.keys()
    sql = "select "
    for index,k in enumerate(fields_names):
        if 'varchar' in fields[k] or 'text' in fields[k]:
            sql+="`"+k+"`,"
        else:
            continue
    sql=sql[:sql.rfind(',')]
    sql+=" from "+tb
    if limit:
        sql+=' limit '+str(limit)
    print sql

def load_data(tb):
    print 'load_data'
    sql = "select count(*) from "+tb;
    count = 0
    results = DataUtil.db_query('online','mydb',sql);
    print results
    if results:
        count = results[0][0]
    while True:
        print count
        break
if __name__=='__main__':
    #get_tb_mapper('project_leads')
    tb = 'project_leads'
    #get_tb_all_fields_sql('project_leads',10)

    load_data(tb)
