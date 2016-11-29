#!/usr/bin/env python
# coding=utf-8
from file_util import *
from data_util import *
from date_util import *

# truncate table attribute_weight;
def job_main():
    print 'Job is running.'
    try:
        file = open('attribute_weight.csv')
        i=0
        while 1:
            line = file.readline()
            i+=1
            print '*'*50,i,'*'*50
            if(i==1):
                continue
            #if i>101: exit(1)
            if not line:
                print 'read end'
                break
            else:
                line_arr = line.split('\t')
                #print line_arr
                category_i1=''
                category_i2=''
                attr=''
                weight = 0.0
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
                        category_i = val
                    elif index==1:
                        category_j = val
                    elif index==2:
                        attribute_i = val
                    elif index==4:
                        weight = float(val)
                #print category_i1,category_i2,category_j1,category_j2
                
                #validate_result = validate_attribute('商业模式','零售电商','实物电商')
                validate_result = validate_attribute(attribute_i,category_j,category_i)
                if validate_result == True:
                    print 'validate ok'
                else:
                    print 'validate error'
                    exit(1)
                sql = "select * from attribute_weight where category_i='{0}' and category_j='{1}' and attribute_i='{2}';".format(category_i,category_j,attribute_i)
                print sql
                check_results = False
                check_exist_results = DataUtil.db_query('irweb','mydb',sql)
                
                if check_exist_results!=None and len(check_exist_results)>0:
                    check_results = True
                    print 'exist'
                else:
                    print 'not exist'
                
                sql = "insert into attribute_weight (category_i,category_j,attribute_i,weight,create_time,status) values('"+category_i+"','"+category_j+"','"+attribute_i+"','"+str(weight)+"','"+now_str+"',"+str(status)+")"
                #print sql
                if not check_results:
                    DataUtil.db_update('irweb','mydb',sql)
                    print 'insert ok'
                #print line
    #except:
    except Exception as err:
        print 'import error!'
        print err
        exit(1)
#
# demo validate_attribute('商业模式','零售电商','实物电商')
def validate_attribute(attr,category_i2,category_i1):
    _results =False
    sql="""
select 
attr_name,cate_name,parent_name,cate_base_id,parent_id as cate_parent_id 
from(
select a.name as attr_name,c.name as cate_name,c.id as cate_base_id 
from category_attribute_def as a inner join category_backend_def as c 
where  c.id = a.categoryId and a.name='{0}' and c.name='{1}' and a.status=0 and c.status=0) 
as t11 
inner join(
select * from ( 
select id as base_id,name as base_name,parent as parent_id from category_backend_def where status=0 ) as t1
inner join  ( select id,name as parent_name from category_backend_def where status=0)  as t2  where t1.parent_id=t2.id and base_name='{1}'and parent_name='{2}')
as t22
where t11.cate_name = t22.base_name;
    """.format(attr,category_i2,category_i1)
    print sql
    results = DataUtil.db_query('online','mydb',sql)
    if results !=None and len(results)>0:
        _results = True
    return _results
        
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
        else:
            print category_i1 +' is not  ' +category_i2+' parent'
            _results=False
    return _results

if __name__=='__main__':
    job_main()
    #r= validate_attribute('商业模式','零售电商','实物电商')
    #print r
