#!/usr/bin/env python
# coding=utf-8
from file_util import *
from data_util import *
from date_util import *

def job_main():
    print 'Job is running.'
    try:
        file = open('category_sim.csv')
        i=0
        while 1:
            line = file.readline()
            i+=1
            print '*'*50,i,'*'*50
            if(i==1):
                continue
            if not line:
                print 'read end'
                break
            else:
                line_arr = line.split('\t')
                #print line_arr
                category_i1=''
                category_i2=''
                category_j1=''
                category_j2=''
                category_sim = 0.0
                now_str = get_today_str()
                status = 1
                sql = ''
                sql1=''
                sql2=''
                parentId=-1
                categoryId=-1
                category_parent_dict = {}
                for index,val in enumerate(line_arr):
                    #print index,val   
                    if index==0:
                        category_i1 = val
                    elif index==1:
                        category_i2 = val
                    elif index==2:
                        category_j1 = val
                    elif index==3:
                        category_j2 = val.decode('utf8','ignore') 
                    elif index==4:
                        category_sim = float(val)
                #print category_i1,category_i2,category_j1,category_j2
                
                validate_result1 = validate_category_sql(category_i1,category_i2)
                validate_result2 = validate_category_sql(category_j1,category_j2)
                if validate_result1==True and validate_result2 == True:
                    print 'validate ok'
                else:
                    print 'category error'
                    exit(1)
                sql = "select * from category_sim where category_i1='{0}' and category_i2='{1}' and category_j1='{2}' and category_j2='{3}'".format(category_i1,category_i2,category_j1,category_j2)
                print sql
                check_results = False
                check_exist_results = DataUtil.db_query('irweb','mydb',sql)
                
                if check_exist_results!=None and len(check_exist_results)>0:
                    check_results = True
                    print 'exist'
                else:
                    print 'not exist'
                sql = "insert into category_sim (category_i1,category_i2,category_j1,category_j2,similarity,create_time,status) values('"+category_i1+"','"+category_i2+"','"+category_j1+"','"+category_j2+"',"+str(category_sim)+",'"+now_str+"',"+str(status)+")"
                #aprint sql
                if not check_results:
                    DataUtil.db_update('irweb','mydb',sql)
                    print 'insert ok'
                #print line
    #except:
    except Exception as err:
        print 'open file error!'
        print err
        exit(1)
def validate_category_sql(category_i1,category_i2):
    _results = False
    sql = """
    select * from (
    select id as base_id,name as base_name,parent as parent_id from category_backend_def where status=0

    ) as t1 
    inner join 
    (
    select id,name as parent_name from category_backend_def where status=0
    ) 
    as t2 
    where t1.parent_id=t2.id and t1.base_name='{0}' and t2.parent_name='{1}'
    """.format(category_i2,category_i1)
    print sql 
    results = DataUtil.db_query('online','mydb',sql)
    if results != None:
        count = len(results)
        if count >0:
            _results = True
    return _results
# unused,has bug
def validate_category(category_i1,category_i2):
    _results = False
    sql1 = "select id,parent from category_backend_def where name='"+category_i1+"' limit 1;"
    sql2 = "select id,parent from category_backend_def where name='"+category_i2+"' limit 1;"
    #print sql1
    results1 = DataUtil.db_query('online','mydb',sql1)
    results2 = DataUtil.db_query('online','mydb',sql2)
    print results1,results2
    if results1==None or len(results1)==0:
        _results=False
        print 'query category error - '+category_i1
        print sql1
    elif results2==None or len(results2)==0:
        _results=False
        print 'query category error - '+category_i2
        print sql2
    else:
        categoryId1 = results1[0][0]
        parentId1 = results1[0][1]
        categoryId2 = results2[0][0]
        parentId2 = results2[0][1]
        if int(parentId2) ==int(categoryId1) and int(parentId1)==0:
            _results = True
        elif int(categoryId1) == int(categoryId2):
            _results = True
        else:
            print category_i1 +' is not  ' +category_i2+' parent'
            _results=False
    return _results

if __name__=='__main__':
    job_main()
    t= get_today_str()
    print t
    print 'end'
