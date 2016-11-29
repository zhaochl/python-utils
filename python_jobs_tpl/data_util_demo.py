# -*- coding: utf-8 -*-
import MySQLdb
import functools
import time
import datetime
import urllib
import urllib2
import Logger
class DataAccess:
###################
    @staticmethod
    def GetDb():
        conn = None
        conn = MySQLdb.connect(host="irweb", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        #conn = MySQLdb.connect(host="localhost", port=4000,user="root", passwd="root",db="root",charset="utf8")
        return conn

    @staticmethod
    def GetDb_project():
        conn = None
        #conn = MySQLdb.connect(host="127.0.0.1", port=3306,user="root", passwd="dashboard54321",db="mydb",charset="utf8")
        #conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        conn = MySQLdb.connect(host="localhost", port=3306,user="root", passwd="root",db="mydb",charset="utf8")
        return conn

    @staticmethod
    def get_investorlist(uid):
        conn = None
        cursor=None
        try:
            conn = DataAccess.GetDb_project()

            cursor = conn.cursor()
            cursor.execute("set NAMES utf8 ")
            sql = "SELECT i.userid,u.name,u.`company` ,i.fundid FROM `mydb`.`investor_info` as i inner join user as u on i.userid=u.userid where i.userid >"+str(uid)+"   ORDER BY i.`userid` LIMIT 1000;"
            print sql
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except MySQLdb.Error, e:
            #logger.info("get url mysqldb error!")
            print "add into cluster mysqldb error! --%d:  %s" % ( e.args[0], e.args[1]   )
            return None
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!= None):
                conn.close()

    @staticmethod
    def get_project_attributes(projectid):
        conn = None
        cursor=None
        try:
            conn = DataAccess.GetDb_project()
            cursor = conn.cursor()
            cursor.execute("set NAMES utf8 ")
            sql = "SELECT projectid,attributeid,value,id FROM `mydb`.`project_category_backend` where projectid= "+str(projectid)+" ORDER BY `id` "
            cursor.execute(sql)
            results = cursor.fetchall()
            return results
        except MySQLdb.Error, e:
            #logger.info("get url mysqldb error!")
            print "add into cluster mysqldb error! --%d:  %s" % ( e.args[0], e.args[1]   )

            return None
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!= None):
                conn.close()


    @staticmethod
    def update_team_info__ (projectid,teaminfo_by_editor):
        cursor = None
        conn = None
        try:
            conn = DataAccess.GetDb()
            cursor = conn.cursor()
            cursor.execute("set NAMES utf8")

            sql ="update team_tab set teaminfo='%s' where projectid=%d;" % (teaminfo_by_editor,projectid)
            print sql#[0:32]

            cursor.execute(sql)
            conn.commit()
            #print 'add ok',projectid

        except MySQLdb.Error, e:
            print 'insert team error:', e.args[0], e.args[1]
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!= None):
                conn.close()

    @staticmethod
    def add_team_categoryinfo(projectid,categorystr,matchedstr,teaminfo_by_editor):
        cursor = None
        conn = None
        try:
            conn = DataAccess.GetDb()
            cursor = conn.cursor()
            cursor.execute("set NAMES utf8")
            existed=DataAccess.get_team(projectid)
            if(existed==0):
                sql ="insert into team_tab(categorystr,catematchedstr,projectid,teaminfo)  values ('%s','%s',%d,'%s');" % (categorystr,matchedstr,projectid,teaminfo_by_editor)
                #sql ="update team_tab set categorystr='%s',catematchedstr='%s' where projectid=%d;" % (categorystr,matchedstr,projectid)
            else:
                sql ="update team_tab set categorystr='%s',catematchedstr='%s' where projectid=%d;" % (categorystr,matchedstr,projectid)
            print sql#[0:32]

            cursor.execute(sql)
            conn.commit()
            #print 'add ok',projectid

        except MySQLdb.Error, e:
            print 'insert team error:', e.args[0], e.args[1]
        finally:
            if(cursor!=None):
                cursor.close()
            if(conn!= None):
                conn.close()


