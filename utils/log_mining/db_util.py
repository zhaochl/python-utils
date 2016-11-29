# -*- coding: utf-8 -*-
import MySQLdb

dbg=False
"""
results = DataUtil.db_query('online','mydb',sql)

"""
def db_query(server,sql,value_list=None):
    conn = None
    cursor=None
    try:
        if server=='irweb':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='online':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='irdev':
            conn = MySQLdb.connect(host="irdev", port=3306,user="root", passwd="123456",db="mydb",charset="utf8")
        elif server=='project':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        else:
            print 'server error,only irweb,online,irdev'
            return None

        cursor = conn.cursor()
        cursor.execute("set NAMES utf8 ")
        if dbg: print sql
        if value_list==None:
            cursor.execute(sql)
        else:
            cursor.execute(sql,value_list)
        results = cursor.fetchall()
        return results
    except MySQLdb.Error, e:
        #logger.info("get url mysqldb error!")
        print "db_query error!sql:%s --%d:  %s" % (sql, e.args[0], e.args[1]   )
        return None
    finally:
        if(cursor!=None):
            cursor.close()
        if(conn!= None):
            conn.close()
"""
DataUtil.db_update('irweb','mydb',sql)
"""
def db_update(server,sql):
    conn = None
    cursor=None
    try:
        if server=='irweb':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='online':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='irdev':
            conn = MySQLdb.connect(host="irdev", port=3306,user="root", passwd="123456",db="mydb",charset="utf8")
        elif server=='project':
            print 'project read only'
            exit()
            #conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        else:
            print 'server error,only irweb,online,irdev'
            return None
        cursor = conn.cursor()
        cursor.execute("set NAMES utf8 ")
        if dbg: print sql
        cursor.execute(sql)
        conn.commit()
    except MySQLdb.Error, e:
        #logger.info("get url mysqldb error!")
        print "db_update error! sql:%s--%d:  %s" % (sql, e.args[0], e.args[1]   )
        return None
    finally:
        if(cursor!=None):
            cursor.close()
        if(conn!= None):
            conn.close()
"""
db_add('irweb','spy_config',data_dict)
"""
def db_add(server,table,data_dict):
    conn = None
    cursor=None
    try:
        if server=='irweb':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='online':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='irdev':
            conn = MySQLdb.connect(host="irdev", port=3306,user="root", passwd="123456",db="mydb",charset="utf8")
        else:
            print 'server error,only irweb,online,irdev'
            return None
        cursor = conn.cursor()
        cursor.execute("set NAMES utf8 ")
        if dbg: print sql
        qmarks = ', '.join(['%s'] * len(data_dict)) 
        cols = ', '.join(data_dict.keys()) 
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
        cursor.execute(sql,data_dict.values())
        conn.commit()
    except MySQLdb.Error, e:
        #logger.info("get url mysqldb error!")
        print "db_update error! sql:%s--%d:  %s" % (sql, e.args[0], e.args[1]   )
        return None
    finally:
        if(cursor!=None):
            cursor.close()
        if(conn!= None):
            conn.close()
"""
return results,_colums
"""
def db_query_info(server,sql):
    conn = None
    cursor=None
    try:
        if server=='irweb':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='online':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        elif server=='irdev':
            conn = MySQLdb.connect(host="irdev", port=3306,user="root", passwd="123456",db="mydb",charset="utf8")
        elif server=='project':
            conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        else:
            print 'server error,only irweb,online,irdev'
            return None
        cursor = conn.cursor()
        cursor.execute("set NAMES utf8 ")
        if dbg: print sql
        cursor.execute(sql)
        descrption = cursor.description
        _colums = []
        for _d in descrption:
            _c = _d[0]
            _colums.append(_c)
        results = cursor.fetchall()
        return results,_colums
    except MySQLdb.Error, e:
        print "db_query_info error! --%d:  %s" % ( e.args[0], e.args[1]   )
        return None
    finally:
        if(cursor!=None):
            cursor.close()
        if(conn!= None):
            conn.close()
"""
colum,results_data,sql
"""
def convert_results(server,sql):
    results,colum = db_query_info(server,sql)
    colum_len = len(colum)
    results_data =[]
    if results!=None:
        for r in results:
            obj ={}
            for i in range(colum_len):
                colum_name = colum[i]
                tmp_row =  r[i]
                obj[colum_name] = str(tmp_row)
            results_data.append(obj)
    return colum,results_data,sql


if __name__=='__main__':
    sql='select count(*) as count from project'
    results,colum = db_query_info('online',sql)
    print results
    print colum
