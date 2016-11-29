#usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
from DataAccess import *
import Logger
import traceback
import UbClient
import mcpack
import time
from datetime import date, timedelta
from collections import defaultdict
import socket
import struct
import redis
import json
import math
from time import sleep
from redis_access import *
import thread


MAX_UTRACK_LEN = 51
_HISTORY=1
_REALTIME=2
_WEEKLY=3

_DEBUG=""
_ABTEST=""

behavior_weight={

    "project_expose":1,
    "project_view":5,
    "apply_meeting":5
}


team_interest_behavior={
    "bp_viewed":1,
    "project_bp##open":1,
    "project_bp##email":1
}



obj_topic_id = re.compile(r'^topic_id')
obj_best_title = re.compile(r'^best_title:')
obj_page_id = re.compile(r'^id:')
obj_delimi = re.compile(r'\t')
topic_list = []
userprofilelogger = Logger.initlog('log_stat_ctr'+_DEBUG)

dbhost = "127.0.0.1" #"10.10.208.13"
dbport = 1883 #int(sys.argv[2])

def writefile(destfileName,data2w):                                                                                                                          
    #wordF= file( destfileName,'w')      
    #print '111dest---',destfileName
    #wordF= open( destfileName,'w+')      
    wordF= file( destfileName,'w')      
    #print 'dest---',destfileName
    wordF.write('%s' %(data2w))     
    wordF.close()

def appendfile(destfileName,data2w):
    wordF= file( destfileName,'a')      
    wordF.write('%s' %(data2w))     
    wordF.close()

def writefile4int(destfileName,iValue):
    wordF= file( destfileName,'w')      
    wordF.write('%d' %(iValue))     
    wordF.close()

def readfile4int(destfileName,iValue):
    wordF= file( destfileName,'w')      
    wordF.write('%d' %(iValue))     
    wordF.close()

def readfile(destfileName):
    if not os.path.exists(destfileName):
        return ""
    singleFile= file( destfileName,'r') 
    singleFile.seek(0)     
    fContent = singleFile.read()
    singleFile.close()
    return fContent



class p_profile:
    def __init__(self): #,_projectid,_viewcount,_updatetime , _bp_viewed_count,_apply_meeting_count,_replied_count,_marked_count,_exposed_count):
        self.projectid                  =0   # _projectid           
        self.viewcount                  =0   # _viewcount           
        self.updatetime                 =0   # _updatetime          
        self.bp_viewed_count            =0   # _bp_viewed_count     
        self.apply_meeting_count        =0   # _apply_meeting_count 
        self.replied_count              =0   # _replied_count       
        self.marked_count               =0   # _marked_count        
        self.exposed_count          =0   # _exposed_count
        self.recommend_count =0   # _exposed_count
        self.like_count =0   # _exposed_count



def getdata(aids):
    pass

#    logger = Logger.initlog('get_url.log')
#    total_num = 0
#    category_num = 0 
#    category_id = 0 
#
#    if(1):
#        results = DataAccess.get_url_by_aid(aids,logger)
#        if results:
#            category_num = 8;#//category_id # category_num + 1
#            try:
#                file_name = "urls_data_cluster/merged_cluster_url8"
#                #+ str(category_num)
#                file_url = open(file_name,'w+')
#
#                for result in results:
#                    publishtime = result[4]
#                    title = result[2].strip()
#                    #print 'default-utf[', title ,"]\n"#= result[2].strip()
#                    title = title.replace('\t',' ')
#                    title = title.replace('\n',' ')
#                    title = title.encode('utf-8','ignore')
#                    #title = title.encode('gbk','ignore')
#                    #print 'original--[',title ,"]\n"#= title.encode('gbk','ignore')
#                    #print  title.encode('utf-8','ignore')
#                    #print  title.decode("utf-8").encode("gbk")
#                    #sleep(3) #summary = result[4].strip()
#                    summary = result[3].strip()
#                    summary = summary.replace('\t',' ')
#                    summary = summary.replace('\n',' ')
#                    #summary = summary.encode('gbk','ignore')
#                    summary = summary.encode('utf-8','ignore')
#                        #l2=len(summary)
#                        #if(l1!=l2):
#                        #    print 'replaced',l1,l2
#                        #    raw_input()
#
#                    url = result[1].strip()
#                    if(url.find("dahe.cn")>0):
#                        continue
#                    url= url.replace('\t',' ')
#                    url= url.replace('\n',' ')
#                    #url = url.encode('gbk','ignore')
#                    url = url.encode('utf-8','ignore')
#                    aid = result[0]
#                    content=summary
#    #                if (len(summary)>1024):
#    #                    try:
#    #                        summary=summary[0:1024]
#    #                    except:
#    #                        print "except",aid
#    #                    finally:
#    #                        pass
#                    if(title and url and publishtime):
#                        file_url.write("%s\t" % (aid))
#                        file_url.write("%s\t%s\t" %(title,summary))
#                        file_url.write("%s\t%s\t%s\n" %(url,publishtime,content))
#                        total_num = total_num + 1
#
#                    else:
#                        logger.info("tile or url or publishtime is null, ignored!")
#            finally:
#                file_url.close()
#    #if res :
        #for category_id in res:
		
    #    else:
    #        logger.info("category: %s get urls null!" %(category_id[0]))
    #else:
    #    logger.info("get category list null!")
    #logger.info("total get urls :%d, category num :%d " %(total_num, category_num)) 


def getparser(title):#,content,aid,pubtime):
    pok=0
    termstr=""
    tryTimes=0;
    __terms=""
    while(tryTimes < 3):
        tryTimes=tryTimes+1
        #try:
        if(1):
            con=None
            if(con==None):
                dbtype = "socket"
                dbfile = ""
                dbwto = 1000
                dbrto = 1000
                logger = Logger.initlog("./con_sock_log")

                con = UbClient.Connector(dbtype, dbhost, dbport, dbfile ,dbwto, dbrto, logger) 
                con.sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        
            reqdata = {}
    
            reqdata["title"]=title  
            reqdata["content"]=title
            reqdata["aid"]=0
            reqdata["pubtime"]=0

            req_pack = mcpack.dumps_version(mcpack.mcpackv1, reqdata, 4*1024*1024)
            con.write_pack(req_pack)
            (ret ,res_pack) = con.read_pack()
            pok=1
            if ret == 0:
                resdict = mcpack.loads(res_pack)
                
                __terms=resdict["terms"].replace("'"," ") 
                __terms = __terms.decode("gbk").encode('utf-8','ignore')  
                __termCount=resdict["termCount"]

                #print title
                #print __terms

#                if(__terms!=""):
#                    #print '-sock-ok',aid,__dupaids
#                    dup_old_id=0
#                    arr = __terms.split(';')
#                    termcount=len(arr)
#
#                    reali=0;
#                    _iterator_lock.acquire()  
#                    _iterator_count+=1
#                    reali=_iterator_count
#                    lock.release() 
#
#                    if(reali % 10001 ==0):
#                        print reali
#
#
#                    if((termcount-1) !=int(__termCount)):
#                        print "count not match",aid,termcount,__termCount
#
#                    termstr=__terms
                break;
    
        #except:
        if(0):
            #print 'except-sock-',sys.exc_info()[0]
            con.sock.close()
            sleep(1)#con.sock.close()
            con=None
    
        if(con!=None):
            con.sock.close()
            con=None

    return __terms,__termCount

class ANode:
    def __init__(self,_sent,_mapdict):
        self.sent=_sent
        self.mapdict=_mapdict

    
def get_abstract(str_aids,keys):
    allstr = "";
    if(str_aids==None or len(str_aids)==0):
        return allstr

    str_aids=str_aids.strip(',')
    results = DataAccess.get_url_by_aid(str_aids,None)

    keyarr=keys.split('|')
    allsents=[]
    if results and len(results)>0:
        #try:
        if(1):

            for result in results:
                content = result[3]
                content=content.replace("\n"," ")
                content = content.encode("utf-8")
                content=content.replace("！","。").replace("？","。")
                sents=content.split("。")[0:5]
                _dict={}
                for s in sents:
                    for k1 in keyarr:
                        k=k1.strip('\t').strip()
                        if(s.find(k)>=0):
                            if(_dict.get(k)==None):
                                _dict[k]=1

                    _anode=ANode(s,_dict)
                    allsents.append(_anode)

            #topsents = sorted(allsents, lambda x, y: cmp(len(x[1]), len(y[1])), reverse=True)[0:20]
            topsents = sorted(allsents, lambda x, y: cmp(len(x.mapdict), len(y.mapdict)), reverse=True)[0:20]
            count=0;
            addedcount=0;
            addedsents=[]
            for s in topsents:

                if(len(s.sent)>256):
                    continue

                if(count==0):
                    allstr+=s.sent+"。| "
                    addedsents.append(s);
                    addedcount+=1;
                else:
                    issame=0;
                    matchedkeycount=0
                    not_matchedkeycount=0
                    for s1 in addedsents:
                        for k in s.mapdict:
                            if(s1.mapdict.get(k)):
                                matchedkeycount+=1
                                if(matchedkeycount>2):
                                    pass
                                    #issame=1
                                    #break;
                            else:
                                not_matchedkeycount+=1
                        if(matchedkeycount*100>((len(s.mapdict)+len(s1.mapdict))*50)):#not_matchedkeycount):
                            issame=1
                            break;
                    if(issame==0):
                        #print 'added more'
                        allstr+=s.sent+"。| "
                        #print allstr
                        addedsents.append(s);
                        addedcount+=1;
                        if(addedcount>2):
                            break;
                    else:
                        #print "no more-------"
                        pass

                count+=1

                
        #except:
            #print 'getsents error--'

    return allstr

def getstocks(str_aids):
    allstr = "";
    if(str_aids==None or len(str_aids)==0):
        return allstr

    str_aids=str_aids.strip(',')
    results = DataAccess.get_stocks_by_aid(str_aids)

    if results and len(results)>0:
            try:

                for result in results:
                    stockname = result[0]
                    allstr+=stockname +" | "
            except:
                print 'getstock error--'

    return allstr


def get_doc(begin,end):
    total_num = 0
    category_num = 0 
    category_id = 0 

    if(1):
        category_id=8
        results = DataAccess.get_url_by_time(begin,end)
        #print results #= DataAccess.get_url_by_time(begin,end)
        if results and len(results)>0:
            #print len(results)
            file_name = "./to_do_file/docs" #+ str(category_num)
            file_url = open(file_name,'w+')
            category_num = category_id # category_num + 1
            try:

                for result in results:
                    publishtime = result[4]
                    #if(cur_time_stamp>publishtime+expire_span):
                    #    continue
                    title = result[2].strip()
                    title = title.replace('\t',' ')
                    title = title.replace('\n',' ')
                    title = title.encode('utf-8','ignore')

                    url = result[1].strip()
                    url= url.replace('\t',' ')
                    url= url.replace('\n',' ')
                    url = url.encode('utf-8','ignore')


                    if(len(title)<17):
                        #print 'title too short',url
                        pass
                    summary = result[3].strip()


                    summary = summary.replace('\t',' ')
                    summary = summary.replace('\n',' ')
                    summary = summary.encode('utf-8','ignore')

                    if(len(summary)<300):
                        continue

            #        for sent in sentence_list:
                        #l1=len(summary)

            #            summary = summary.replace(sent," ")
                        #l2=len(summary)
                        #if(l1!=l2):
                        #    print 'replaced',l1,l2
                        #    raw_input()


                    wapurl = ""
                    if(result[5]!=None):
                        wapurl = result[5].strip()
                        wapurl = wapurl.encode('utf-8','ignore')

                    aid = result[0]
                    content=summary
                    maxlen=3000
#                    if (len(summary)>maxlen):
#                        try:
#                            summary=summary[0:maxlen]
#                        except:
#                            print "except",aid
#                        finally:
#                            pass
                    if(title and url and publishtime):
                        file_url.write("%s\t" % (aid))
                        file_url.write("%s\t%s\t" %(title,summary))
                        file_url.write("%s\t%s\t%s\t%s\n" %(url,publishtime,content,wapurl))
                        total_num = total_num + 1

                    #else:
                    #    print "tile or url or publishtime is null, ignored!"
            finally:
                file_url.close()

#def do_cluster(begin,end):
#    try:
#        get_doc(begin,end)#begin_timeStamp,end_timeStamp )
#        destdir="./daily_cluster_result/"+time.strftime("%Y_%m/%d_%H_%M_%S", time.localtime(begin))
#        os.system("mkdir -p "+destdir)
#        print 'begin cluster'
#        os.system("sh -x do_cluster.sh "+destdir+"/docs")
#    except:
#        print "do_cluster error"
#


#def teestd():
#    allstr = "";
#    item_num = 1
#    flag = 0
#    eventid=0
#    try:
#        curtimestamp=time.time()
#        begin_of_week_timestamp=0 #curtimestamp-3600*24
#        end_of_thisweek_timestamp=0 #curtimestamp-3600*24
#
#
#        if(1):
#
#                    createtime1 = time.strptime("2015-8-24", "%Y-%m-%d")        
#                    print 'createtime__1',createtime1
#                    #createtime = datetime()
#                    #sql = " SELECT eventid,userid,projectid,type,creationtime,fromstatus,tostatus,createby  FROM `mydb`.`project_investor_event` where eventid > "+str(eventid)+" ORDER BY `eventId` LIMIT 50;"
#
#                    #weekday=createtime.weekday()
#                    #print createtime,'weekday',weekday 
#
#
#                    createtime="2015-8-23 23:23:10"
#                    timeArray = time.strptime(str(createtime) , "%Y-%m-%d %H:%M:%S")        
#                    print 'timeArray --' , timeArray 
#
#                    #dateArray = time.strptime(str(createtime) , "%Y-%m-%d %H:%M:%S")        
#                    current_timeStamp = int(time.mktime(timeArray))    
#                    if(begin_of_week_timestamp==0 or current_timeStamp > end_of_thisweek_timestamp):
#                        if(begin_of_week_timestamp != 0 and current_timeStamp > end_of_thisweek_timestamp):
#                        #if(current_timeStamp > end_of_thisweek_timestamp):
#                            pass
#                            print "pass this week 's data"
#
#                        begin_of_week_timestamp=current_timeStamp 
#                        date_time_=time.localtime(begin_of_week_timestamp)
#                        tmy=date_time_.tm_year
#                        tmm=date_time_.tm_mon
#                        tmd=date_time_.tm_mday
#
#                        tmw=date_time_.tm_wday
#                        zero_of_thisday=datetime.datetime(tmy,tmm,tmd)
#
#                        print 'zero_of_thisday', zero_of_thisday
#
#
#                        timeArray_end = time.strptime(str(zero_of_thisday) , "%Y-%m-%d %H:%M:%S")        
#                        zero_timeStamp = int(time.mktime(timeArray_end ))    
#                        end_of_thisweek_timestamp= zero_timeStamp + (7-tmw)*24*3600-1
#                        end_date_time_=time.localtime(end_of_thisweek_timestamp)
#                        print 'end_date_time_:',  end_date_time_
#
#                        pass
#
#
#
#
#
#    except:
#        print "traceback", traceback.print_exc()
#        logger.info("read file urls/* failed!")
#    finally:
#        pass
#


global_user_project_dict={}
global_user_localhost={}


def newly_changed_project():
    total_num = 0
    category_num = 0 
    category_id = 0 
    all_sentimental = 0 
    global_aid=0
    pid=0

    commonsentf="./common_sents_4_project"
    common_sents=readfile(commonsentf)
    commarr=common_sents.split("\n")
    common_dict={}
    for s1 in commarr:
        s=s1.strip()
        #print s
        if(not common_dict.has_key(s)):
            common_dict[s]=1


#    lastmaxid=0
#    last_projectid_file="./lastid_record_move_project"
#    strLastImageid=readfile(last_projectid_file)
#    if(strLastImageid is not ""):
#        lastmaxid=(int)(strLastImageid)


    tableid=""
    results = DataAccess.get_tableid()

    if results==None or len(results)==0:
        #print 'no result tableid'
        pass

    if results:
        for result in results:
            tableid= result[0].encode('utf-8','ignore')
            break

    #print 'tableid['+tableid+']'

    if(tableid==""):
        tableid="2"
    else:
        tableid=""


    data_process_success=0
    while(1):
        results = None
        if(for_history):
            results = DataAccess.get_project_online_once(pid)
        else:
            results = DataAccess.get_project_online(pid)
            #print 'should update'
            #results = DataAccess.get_project_online_debug(pid)

        if results==None or len(results)==0:
            #print 'no result',pid
            break
            #sleep(150)
            #continue
            
        #print 'result len:',len(results),' pid:',pid

        if results:
            con=None
            try:
                data_process_success=1

                #print 'result count:',len(results)

                for result in results:
                    projectid = result[0]
                    title = result[1].strip()
                    title = title.replace('\t',' ')
                    title = title.replace('\n',' ')
                    title = title.encode('utf-8','ignore')

                    field=field.lower()
                    farr=field.replace("，",",").split(',')
                    fieldliststr=""
                    categoryindex=0;
                    
                    querystr=""

                    #here we can get category (begin with T_parent_cat_+sub_catename)
                    #here we can get attribute (begin with K_+attribute name)

                    catestr,attributestr,qstr,kdstr,_cid=get_project_attribute(projectid,categoryid )


#                    if(categoryid != _cid and _cid>0): 
#                        print 'error----projectid:',projectid, 'categoryid:', categoryid,'_cid',_cid
#                        raw_input()

                    if(categoryid and categoryid > 0 and (catestr==None or len(catestr)<5)):
                        p_s_k=get_parent_subcate(categoryid)
                        if(p_s_k ):
                            p_s_k=p_s_k.strip()
                            if(len(p_s_k)):
                                catestr="T1="+p_s_k+"\tTw1=1\t"
                                querystr+=p_s_k+"\t1\t"
                                #print 'only cate,no attribute',catestr
                                #raw_input()



                    cate_dict=defaultdict(int)
                    for f1 in farr:
                        f=f1.strip()
                        if(f and len(f)>0):
                            #fieldliststr += f+" "
                            cate_dict[f]=1
                            #print 'category is ',f
                            categoryindex+=1
                            fieldliststr +="t"+str(categoryindex)+ "=t_"+f+"\t"+  "tw"+str(categoryindex)+ "=1\t"  #"+str(termweight) +"\t"
                            querystr+="t_"+f+"\t1\t"

                            #fieldliststr +="t"+str(categoryindex)+ "="+f+"\t" #+  "tw"+str(categoryindex)+ "=1\t #"+str(termweight) +"\t"
                           # flist.append(f)
                            #termstr+="k"+str(realtindex)+ "="+termarr[tindex]+"\t"+  "kw"+str(realtindex)+ "="+str(termweight) +"\t"


                    if(title):
                            
                        fieldliststr=fieldliststr.strip()

                        content=summary+ " "+content
                        title=title.lower();


                        #content=content.replace("content","");
                        #content=content.replace("title","");
                        content=content.replace("暂无","");
                        sentlist=getallsents(content)

#                        if(content.find("【项目介绍】")>=0):
#                            print content
#
#                            print sentlist
#                            keys="【项目介绍】"
#                            if(common_dict.has_key(keys)):
#                                print 'haskeys="【项目介绍】"'
#                            else:
#                                print 'not haskeys="【项目介绍】"'
#
#                            print 'common len',len(common_dict)
#                            for sent2 in sentlist:
#                                sent=sent2.strip()
#                                print 'single',sent
#                                if(common_dict.has_key(sent)):
#                                    print 'filtered',sent
#                                    continue
#                            raw_input()

                        realcontent=""
                        for sent2 in sentlist:
                            sent=sent2.strip()
                            if(common_dict.has_key(sent)):
                                #print 'filtered',sent
                                continue

                            realcontent += sent+" "

                        #print 'original',content
                        #print 'afer filter',realcontent
                        content=realcontent.strip()
                        #print content
                        #raw_input()
                        #continue

                        content=content.lower();


                        while(1):
                        #if(1):
                            pos=content.find("http")
                            #print 'http pos',pos
                            
                            if(pos>=0):
                                posend=pos
                                c=content[posend:posend+1]
                                while((c >='a' and c <= 'z') or (c>='0' and c <='9') or c=='/' or c == "_" or c =='?' or c == '&' or c =='.' or c==':'):
                                    posend+=1
                                    c=content[posend:posend+1]

                                url=content[pos:posend]
                                #print 'url:',url,content
                                content=content[0:pos]+" "+content[posend:]
                                #print 'remove url',content
                                #raw_input()
                            else:
                                break



                        while(1):
                        #if(1):
                            pos=content.find("www")
                            #print 'http pos',pos
                            
                            if(pos>=0):
                                posend=pos
                                c=content[posend:posend+1]
                                while((c >='a' and c <= 'z') or (c>='0' and c <='9') or c=='/' or c == "_" or c =='?' or c == '&' or c =='.' or c==':'):
                                    posend+=1
                                    c=content[posend:posend+1]

                                url=content[pos:posend]
                                #print 'url:',url,content
                                content=content[0:pos]+" "+content[posend:]
                                #print 'remove url',content
                                #raw_input()
                            else:
                                break

                                

                        termcount,terms,con=getparser(title,content,con)
                        terms=terms.strip()

                        #print 'count & terms:',termcount,terms
                        #fieldliststr=fieldliststr.lower()

                        total_termweight=0;
                        termstr=""
                        realtindex=0
                        tindex=0

                        terms=terms.strip("\t").strip()
                        if(len(terms)>1):
                            termarr=terms.split("\t")

                            try:
                                highestweight=0
                                while(tindex<len(termarr)):
                                    tarr=termarr[tindex].split(' ')
                                    #tarr=t.split(' ')
                                    k=tarr[0]
                                    termweight=int(tarr[1])
                                    if(highestweight<termweight):
                                        highestweight=termweight


                                    if(cate_dict.has_key(k)):
                                        termweight+=highestweight
                                        #print '00000--term weight boost',termweight

                                    total_termweight+=termweight*termweight
                                    tindex+=1
                            except:
                                print 'except',projectid ,terms,tindex,len(termarr),termarr,len(terms)

                            f_total_termweight=float(total_termweight);
                            f_total_termweight=math.sqrt(f_total_termweight)

                            tindex=0
                            keywordstr_=""
                            while(tindex<len(termarr)):
                                tarr=termarr[tindex].split(' ')
                                termweight=int(tarr[1])

                                if(cate_dict.has_key(tarr[0])):
                                    termweight+=highestweight
                                    #print 'term weight boost',termweight


                                if(f_total_termweight<0.001):
                                    termweight=0.0
                                else:
                                    termweight /=f_total_termweight
                                #termstr+="k"+str(realtindex)+ "="+termarr[tindex]+"\t"+  "kw"+str(realtindex)+ "="+termarr[tindex+1]+"\t"

                                realtindex+=1
                                termstr+="k"+str(realtindex)+ "="+tarr[0] +"\t"+  "kw"+str(realtindex)+ "="+str(termweight) +"\t"
                                querystr+=tarr[0]+"\t"+ str(termweight)+"\t"
                                keywordstr_+=tarr[0]+"\t"

                                #tindex+=2
                                tindex+=1

                        querystr=qstr+querystr
                        #keywordstr_=kdstr+keywordstr

                        querystr=querystr.strip('\t').strip()
                        keywordstr_=keywordstr_.strip('\t').strip()
                        catestr=catestr.strip('\t').strip()
                        attributestr=attributestr.strip('\t').strip()
                        if(for_history):
                            DataAccess.add_project_for_viewed_history(projectid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,creationtime,updatetime,keywordstr_)
                        else:
                            DataAccess.add_project(projectid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,creationtime,updatetime,keywordstr_,tableid)
                            DataAccess.add_project_for_viewed_history(projectid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,creationtime,updatetime,keywordstr_)


                        global_aid += 1

                        #file_url.write("%d %s %s " % (global_aid,aid,url))
                        #file_url.write("%d\t" % (projectid)) #,aid,url))
                        #file_url.write("%s\n" %(terms))



                        #feature_file.write("%d\t%s\t%s\n" % (projectid,title,content))
                        #project_keyword_file.write("%d\t[title:%s]\t[field:%s]\t[keyword:%s]\r\n" % (projectid,title,field,terms))

                        total_num = total_num + 1


                    #else:
                    #    logger.info("tile or url or publishtime is null, ignored!")

                if(projectid > pid):
                    pid=projectid 

            finally:
                #print 'over--',pid
                pass

            if(projectid > lastmaxid):
                lastmaxid=projectid 
                writefile4int(last_projectid_file,lastmaxid)

                        
#    #print 'total_num ', total_num 
#    if(data_process_success and total_num > 50):
#        if(not for_history):
#            DataAccess.update_alter_tab(tableid)
#
    #print 'real over--',pid


user_with_new_interest_dict={}
#def get_user_with_new_interest_dict():
#    global user_with_new_interest_dict
#
#    total_num = 0
#
#    pid=0
#
#    while(1):
#        results = DataAccess.get_user_with_new_interest_dict(pid)
#
#        if results==None or len(results)==0:
#            break;
#
#        if results:
#            try:
#
#                print 'get_user_with_new_interest_dict result count:',len(results),total_num ,pid
#
#                for result in results:
#                    try:
#                        #sql = " select id,frontcat,backcat,attr,attrcontent,subcat from CategoryAttr where id > "+str(id)+" order by id limit 100 ; " 
#                        userid = result[0]
#                        pid = userid 
#                        user_with_new_interest_dict[userid ]=1
#
#                    except:
#                        print "traceback", traceback.print_exc() ,pid
#
#            finally:
#                pass
#
#
                        
    #print 'project count',total_num 




front_back_mapping={}
def get_mapping_back_front_cate():
    global front_back_mapping

    total_num = 0

    pid=0

    while(1):
        results = DataAccess.get_front_back_mapping(pid)

        if results==None or len(results)==0:
            break;

        if results:
            try:

                print 'result count:',len(results),total_num ,pid

                for result in results:
                    try:
                        #sql = " select id,frontcat,backcat,attr,attrcontent,subcat from CategoryAttr where id > "+str(id)+" order by id limit 100 ; " 
                        id = result[0]
                        pid = id

                        frontcat= result[1]
                        if(frontcat==None):
                            continue

                        backcat = result[2]
                        attributeavlue= result[4]
                        subsidiarycat = result[5]

                        frontcat= frontcat.encode('utf-8','ignore').strip()


                        mappingkey=""
                        if(subsidiarycat != None and len(subsidiarycat)>1 ):
                            subsidiarycat = subsidiarycat.encode('utf-8','ignore').strip()
                            mappingkey="T_"+subsidiarycat 
                        elif(attributeavlue!= None and len(attributeavlue)>1 ):
                            attributeavlue= attributeavlue.encode('utf-8','ignore').strip()
                            mappingkey="K_"+attributeavlue
                            pass
                        elif(backcat != None and len(backcat)>1 ):
                            backcat= backcat.encode('utf-8','ignore').strip()
                            mappingkey="T_"+backcat
                            pass
                            
                        back_dict={}
                        if(front_back_mapping.has_key(frontcat)):
                            back_dict=front_back_mapping[frontcat]
                        else:
                            front_back_mapping[frontcat]=back_dict

                        back_dict[mappingkey]=1

                    except:
                        print "traceback", traceback.print_exc() ,pid

            finally:
                pass


                        
    #print 'project count',total_num 




firstround_init=0


def get_tableid():

    tableid=""
    #print 'inner#######get_project_profile'

    results = DataAccess.get_tableid()

    if results==None or len(results)==0:
        ###print 'no result tableid'
        pass

    if results:
        for result in results:
            tableid= result[0].encode('utf-8','ignore')
            #print "tableid= result[0].encode('utf-8','ignore')"
            break
    return tableid

def get_project_profile_newly_changed():
    for_new_changed_data=1
    get_project_profile(for_new_changed_data)




def get_user_localhost():
    global global_user_localhost

    total_num = 0
    #logid=0
    uid =0

    while(1):
        results = DataAccess.get_user_localhost(uid)
        #print 'need to rm project count',total_num 

        if results==None or len(results)==0:
            sleep(3)
            continue

        if results:
            try:
                #currenttimestamp=int(time.time())
                for result in results:
                    try:
                        uid = result[0]
                        company = result[1]
                        if(company ==None or company == ""):
                            continue

                        company = company.encode('utf-8','ignore').strip()
                        if(company != "以太资本"):
                            continue

                        global_user_localhost[uid]=1

                    except:
                        print "traceback", traceback.print_exc() ,logid

            finally:
                pass





load_all_exposed_viewed=0
def get_user_exposed_viewed_project():
    global global_user_project_dict
    global load_all_exposed_viewed

    total_num = 0
    logid=0

    while(1):
        results = DataAccess.get_user_exposed_viewed_project(logid)
        #print 'need to rm project count',total_num 

        if results==None or len(results)==0:
            load_all_exposed_viewed=1
            sleep(1)
            continue

        if results:
            try:
                #print 'get_user_exposed_viewed_project result count:',len(results)
                currenttimestamp=int(time.time())
                for result in results:
                    try:
                        #sql = " SELECT id,userid,projectid,source FROM `mydb`.`investor_project_list` where id > "+str(logid)+" ORDER BY `id` LIMIT 0,50;"
                        logid = result[0]
                        userid = result[1]
                        projectid= result[2]
                        source = result[3]

                        k=str(userid)+"_"+str(projectid)
                        #if(global_user_project_dict.has_key(k)):
                        if(0): 
                            print 'error global_user_project_dict.has_key(k)):has key',k,logid
                            os._exit(1);
                        else:
                            v=[source,currenttimestamp]
                            global_user_project_dict[k]=v
                        #print 'global_user_project_dict',len(global_user_project_dict.keys())

                    except:
                        print "traceback", traceback.print_exc() ,logid

            finally:
                pass


#@profile
def business_contrl():
    global global_user_project_dict
    global _ABTEST
    global global_user_localhost

    eventid=0
    #eventid_new_interest=109000
    last_projectid_file="./lastid_stat_ctr_eventid"+_DEBUG

    lastmaxid=0

    strLastImageid=readfile(last_projectid_file)
    strLastImageid=strLastImageid.strip()
    if(strLastImageid is not ""):
        try:
            lastmaxid=(int)(strLastImageid)
            eventid=lastmaxid
        except:
            print "traceback", traceback.print_exc()

    begineventid=1
    if(eventid<begineventid):
        eventid=begineventid

    iteratorindex=0


    hour_source_dict={}
    hour_source_dict_abtest={}
    batch_over=0

    batch_last_logid=0
    results = DataAccess.get_event_track_new_interest_last_logid()
    if results and len(results)>0:
        for result in results:
            batch_last_logid= result[0]
            break

    if(batch_last_logid>0):
        batch_last_logid-=50;
    print 'batch_last_logid',batch_last_logid


    while(1):

        results = DataAccess.get_event_track_new_interest(eventid)

        if results==None  or len(results)==0:
            #print 'no result business control',eventid ,'curmode',current_mode #last_updated_eventid
            sleep(5);
            continue
            #break;

        if results and len(results)>0:
            #print 'results ', len(results),'eventid_new_interest',eventid_new_interest
            try:

                for result in results:
                    #print 'result:',len(result)
                    #print 'press any key'
                    #raw_input()

                    try:
                        #sql = " SELECT logid,userid,objectid,type,creationtime,subtype,strvalue2 FROM `mydb`.`investor_app_log` where logid > "+str(logid)+" ORDER BY `logId` LIMIT 0,500;"
                        _eventid= result[0]

                        eventid=_eventid

                        userid= result[1]

                        if(global_user_localhost.has_key(userid)):
                            #print 'ether cap user'
                            continue

                        projectid= result[2]
                        if(projectid<=0): continue
                        behaviortype= result[3]

                        if(not behaviortype):
                            continue

                        behaviortype= behaviortype.encode('utf-8','ignore')
                        behaviortype=behaviortype.lower()
                        behaviortype=behaviortype.strip()
                        behaviortype=behaviortype.strip('\t')

                        if(not behavior_weight.has_key(behaviortype)):
                            continue

#                        if(behaviortype=="viewed" or behaviortype=="project_view" ):
#                            inc_viewed=1
#                        elif(behaviortype=="exposed" or behaviortype=="project_expose" ):
#                            inc_exposed=1
#                        elif(behaviortype=="exposed" or behaviortype=="project_expose" ):
#                            inc_exposed=1
#                        else:
#                            continue

                        createtime = result[4]

#                        if(behaviortype=="viewed" or behaviortype=="project_view" ):
#                            inc_viewed=1
#                        elif(behaviortype=="exposed" or behaviortype=="project_expose" ):
#                            inc_exposed=1
#                        else:
#                            continue


                        subtype= result[5]
                        if(subtype!= None):
                            subtype= subtype.encode('utf-8','ignore')
                            subtype=subtype.lower()
                        else:
                            subtype=""


                        inc_viewed=0
                        inc_exposed=0
                        inc_meeting=0


#                        #shoud rm later
#                        if(behaviortype=="apply_meeting" and subtype=="submit" ):
#                            #inc_meeting=1
#                            print "inc_meeting=1"
#                            #raw_input()
#                        else:
#                            continue
#

                        if(behaviortype=="viewed" or behaviortype=="project_view" ):
                            inc_viewed=1
                        elif(behaviortype=="exposed" or behaviortype=="project_expose" ):
                            inc_exposed=1
                        elif(behaviortype=="apply_meeting" and subtype=="submit" ):
                            inc_meeting=1
                            #print "#######need to rm minc_meeting=1"
                        else:
                            continue


                        #filterinterest_for_new=""

                        if(eventid%30001==0):
                            #print '--eventid',eventid,time.strftime("%Y-%m-%d %H:%M:%S")        
                            userprofilelogger.info('--eventid-'+str(eventid)+"---"+str(time.strftime("%Y-%m-%d %H:%M:%S")))

                        occurhour= datetime.datetime.strftime(createtime, '%Y%m%d%H')
                        occurhour=int(occurhour)
                        #print hourformat,type(hourformat)

                        trytimes=0
                        k=str(userid)+"_"+str(projectid)
                        _source=100

                        while(trytimes<3):
                            trytimes+=1

                            if(global_user_project_dict.has_key(k)):
                                v=global_user_project_dict[k]
                                #v=[source,currenttimestamp]
                                _source=v[0]

                                currenttimestamp=int(time.time())
                                v[1]=currenttimestamp
                                break
                            if(eventid<batch_last_logid):
                                break;
                            sleep(1)


                        if((inc_viewed > 0 or inc_exposed>0 or inc_meeting> 0 )):


                            if(batch_over==0 and eventid>batch_last_logid):
                                #flush memory record to db
                                batch_over=1
                                #update data in dict to db

                                for k ,v_e_m in hour_source_dict.items():
                                    arr=k.split('_')
                                    _h=int(arr[0])
                                    _s=int(arr[1])
                                    DataAccess.add_ctr_stat_tab(v_e_m[0],v_e_m[1],_h,_s,_DEBUG,v_e_m[2])

                                for k ,v_e_m in hour_source_dict_abtest.items():
                                    arr=k.split('_')
                                    _h=int(arr[0])
                                    _s=int(arr[1])
                                    DataAccess.add_ctr_stat_tab_abtest(v_e_m[0],v_e_m[1],_h,_s,_DEBUG,v_e_m[2])


                            if(batch_over==0 and eventid<batch_last_logid):
                                #old record,just put into mem and then flush to db later

                                k=str(occurhour)+"_"+str(_source)
                                if(hour_source_dict.has_key(k)):
                                    v_e_m=hour_source_dict[k]
                                    v_e_m[0]+=inc_viewed 
                                    v_e_m[1]+=inc_exposed
                                    v_e_m[2]+=inc_meeting
                                else:
                                    v_e_m=[inc_viewed ,inc_exposed, inc_meeting]
                                    hour_source_dict[k]=v_e_m

                                #if not in realtime mode,just update in memory,only update db in realtime mode; and when the status changed (from history to realtime mode)
                            else:
                                DataAccess.add_ctr_stat_tab(inc_viewed,inc_exposed,occurhour,_source,_DEBUG,inc_meeting)
                            #sql ="select aid from ctr_stat_abtest_tab"+debugstr+" where occurhour="+str(occurhour)+" and source="+str(source)+";"
                            #sql ="insert into ctr_stat_tab"+debugstr+" (viewcount,exposedcount,occurhour,source,meetingcount) values (%d,%d,%d,%d,%d);" % (inc_viewed,inc_exposed,occurhour,source,inc_meeting)


                            abc_test=0
                            if(userid%3==0):
                                abc_test=0
                            elif(userid%3==1):
                                abc_test=1
                            else:
                                abc_test=2


                            if(_source==1):
                                _source+=abc_test

                            if(batch_over==0 and eventid<batch_last_logid):
                                #old record,just put into mem and then flush to db later

                                k=str(occurhour)+"_"+str(_source)

                                if(hour_source_dict_abtest.has_key(k)):
                                    v_e_m=hour_source_dict_abtest[k]
                                    v_e_m[0]+=inc_viewed 
                                    v_e_m[1]+=inc_exposed
                                    v_e_m[2]+=inc_meeting
                                else:
                                    v_e_m=[inc_viewed ,inc_exposed, inc_meeting]
                                    hour_source_dict_abtest[k]=v_e_m
                            else:
                                DataAccess.add_ctr_stat_tab_abtest(inc_viewed,inc_exposed,occurhour,_source,_DEBUG,inc_meeting)


                            #sql ="insert into ctr_stat_abtest_tab"+debugstr+" (viewcount,exposedcount,occurhour,source,meetingcount) values (%d,%d,%d,%d,%d);" % (inc_viewed,inc_exposed,occurhour,source,inc_meeting)

                        if(batch_over==1):
                            writefile4int(last_projectid_file,eventid)
                   
                    except:
                        print "inner traceback", traceback.print_exc()




            except:
                print "traceback", traceback.print_exc()



#    except:
#        print "traceback", traceback.print_exc()
#    finally:
#        pass
#


def process(filename):
    pass

#    global topic_list
#    detail = {}
#    pages = [] #the pages in this topic
#    allstr = "";
#    item_num = 1
#    flag = 0
#    try:
#        fname= "./urls_data_cluster/result_merged_cluster_url24_0"
#        file_topic = open(fname)
#        straids=readdata(file_topic,fname)
#
#        fname= "./urls_data_cluster/result_merged_cluster_url48_24"
#       # file_topic = open(fname)#"./urls_data_cluster/result_merged_cluster_url48_24")
#       # straids_old=readdata(file_topic,fname)
#        #print straids,len(straids_old),type(straids_old),straids_old
#       # straids+=","+straids_old
#
#        if(len(straids)>0):
#            getdata(straids)
#
#        #wfilename = filename.replace("result_url","afterfiltered_");
#        #print wfilename
#        #writefile(wfilename,allstr);
#
#    except:
#        print "traceback", traceback.print_exc()
#        #print 'except--',sys.exc_info()[0]
#        logger.info("read file urls/* failed!")
#    finally:
#        pass

if __name__ == "__main__":
    #dir_path = './urls_data_cluster/'
    #files  = os.listdir(dir_path)
    #teestd()

    #print "sys.exit()"
    #sys.exit()

    if(len(sys.argv)>1):
        print sys.argv[1]
        if(sys.argv[1]=='_debug'):
            _DEBUG=sys.argv[1]
        elif(sys.argv[1]=='abtest'):
            #_DEBUG=sys.argv[1]
            _ABTEST=1
            #update_redis_debug(_DEBUG)
    else:
        trytimes=0
        while(trytimes<3):
            print 'start with online version'
            sleep(3)
            trytimes+=1
        print 'really not input the _debug parameter?'
    #    sleep(15)

    #get_mapping_back_front_cate()
    #get_user_with_new_interest_dict()

    #process("")#dir_path + filename)

    #get_project_profile()

    #print 'should rm the comments'
    #ident1=thread.start_new_thread(get_project_profile_increment,())  
    #get_project_profile_increment()

    #for_new_changed_data=1
    #get_project_profile(for_new_changed_data)
    #thread.start_new_thread(get_project_profile_newly_changed,())  

    thread.start_new_thread(get_user_exposed_viewed_project,())  

    thread.start_new_thread(get_user_localhost,())  

    while(load_all_exposed_viewed==0):
        print 'still in the process of load_all_exposed_viewed'
        userprofilelogger.info('------still in the process of load_all_exposed_viewed----'+str(time.strftime("%Y-%m-%d %H:%M:%S")))
        sleep(3)

    while(1):
        #print '----------------------- buzcontrl 11',time.strftime("%Y-%m-%d %H:%M:%S")        
        userprofilelogger.info('----------------------- ctr begin --'+str(time.strftime("%Y-%m-%d %H:%M:%S")))
        ret=business_contrl()
        #currently it's in realtime mode,switch to weekly mode
        #userprofilelogger.info('-----------------------buzcontrl 000 inner--'+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"--"+str(ret))
        #if(ret==_REALTIME):
        #    userprofilelogger.info('-----------------------buzcontrl 22 '+str(time.strftime("%Y-%m-%d %H:%M:%S")))
        #    ret=business_contrl(_WEEKLY)

    #for filename in files:
    #    topic_list = []
    #if re.match(re.compile(r'^result_url'),filename):


    print 'over--'
