#!/usr/bin/env python
# coding=utf-8
import MySQLdb
CONST_DB_CONFIG ={
    'online_w':{
        'host':'localhost',
        'port':3306,
        'user':'root',
        'passwd':'root',
        'db':'mydb'
    },
}

"""
db_add('irweb','spy_config',data_dict)
"""
def db_add(server,table,data_dict,dbg=False):
    conn = None
    cursor=None
    db_config = {}
    insert_id=-1
    if CONST_DB_CONFIG.has_key(server):
        db_config = CONST_DB_CONFIG[server]
    else:
        raise Exception('Not support server type')
        return None
    try:
        conn = MySQLdb.connect(host=db_config['host'], port=db_config['port'],user=db_config['user'], passwd=db_config['passwd'],db=db_config['db'],charset="utf8")
        cursor = conn.cursor()
        cursor.execute("set NAMES utf8 ")
        qmarks = ', '.join(['%s'] * len(data_dict)) 
        cols = ', '.join(data_dict.keys()) 
        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table, cols, qmarks)
        if dbg: print sql
        cursor.execute(sql,data_dict.values())
        #int(cursor.lastrowid)
        insert_id = int(conn.insert_id())
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
    return insert_id
"""
sql = select title from project where projectId >%s
value_list=[pid]
results = db_query('online',sql,value_list)

"""
def db_query(server,sql,value_list=None,dbg=False):
    conn = None
    cursor=None
    db_config = {}
    if CONST_DB_CONFIG.has_key(server):
        db_config = CONST_DB_CONFIG[server]
    else:
        raise Exception('Not support server type')
        return None

    try:
        conn = MySQLdb.connect(host=db_config['host'], port=db_config['port'],user=db_config['user'], passwd=db_config['passwd'],db=db_config['db'],charset="utf8")

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
return results,_colums
"""
def db_query_info(server,sql,dbg=False):

    conn = None
    cursor=None
    db_config = {}
    if CONST_DB_CONFIG.has_key(server):
        db_config = CONST_DB_CONFIG[server]
    else:
        raise Exception('Not support server type')
        return None

    try:
        conn = MySQLdb.connect(host=db_config['host'], port=db_config['port'],user=db_config['user'], passwd=db_config['passwd'],db=db_config['db'],charset="utf8")
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



"""
DataUtil.db_update('irweb','mydb',sql)
"""
def db_update(server,sql,dbg=False):
    conn = None
    cursor=None
    db_config = {}
    if CONST_DB_CONFIG.has_key(server):
        db_config = CONST_DB_CONFIG[server]
    else:
        raise Exception('Not support server type')
        return None
    try:
        conn = MySQLdb.connect(host=db_config['host'], port=db_config['port'],user=db_config['user'], passwd=db_config['passwd'],db=db_config['db'],charset="utf8")
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
db_update('irweb','spy_config',data_dict)
data = {'sessionEnd':'1'}
where = {'logId':logId}
db_update_data('online','search_query_log',data,where)
"""
def db_update_data(server,table,data_dict,where_dict=None):

    conn = None
    cursor=None
    db_config = {}
    if CONST_DB_CONFIG.has_key(server):
        db_config = CONST_DB_CONFIG[server]
    else:
        raise Exception('Not support server type')
        return None
    try:
        conn = MySQLdb.connect(host=db_config['host'], port=db_config['port'],user=db_config['user'], passwd=db_config['passwd'],db=db_config['db'],charset="utf8")
        cursor = conn.cursor()
        cursor.execute("set NAMES utf8 ")
        data_key = data_dict.keys()
        qmarks = ', '.join([x+'=%s' for x in data_key]) 
        #print qmarks
        where_str=''
        if where_dict!=None:
            where_key_list=where_dict.keys()
            where_k_str = where_key_list[0]
            where_val_list = where_dict.values()
            where_v_str = where_val_list[0]
            if type(where_v_str)==str:
                where_v_str = "'" + where_v_str +"'"
            else:
                where_v_str = str(where_v_str)
            where_str+=where_k_str + '=' +where_v_str
        sql = "update %s set  %s where %s " % (table, qmarks,where_str)
        #print sql
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
