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


DECREMENT_STEP=0.88
MAX_UTRACK_LEN = 51
_HISTORY=1
_REALTIME=2
_WEEKLY=3

_DEBUG=""

behavior_weight={
    "viewed":5,
    "bp_viewed":5,
    "apply_meeting":15,
    "replied":10,
    #"recommended":0,
    "marked":15,
    "like":10,
    "exposed":0,

    "project_expose##":0,
    "project_view##":5,
    "collect_project##collect":10,
    "project_bp##open":5,
    "project_bp##email":5,
    "apply_meeting##":15,
    "filter_label__##":10
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
userprofilelogger = None #Logger.initlog('log_userprofile'+_DEBUG)

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


def getlastid(fname):
    eventid=0 
    strLastImageid=readfile(fname)
    strLastImageid=strLastImageid.strip()
    if(strLastImageid is not ""):
        try:
            lastmaxid=(int)(strLastImageid)
            eventid=lastmaxid
        except:
            print "traceback", traceback.print_exc()

    return eventid


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



global_project_dict={}
global_project_dict_front={}



user_with_new_interest_dict={}
def get_user_with_new_interest_dict():
    global user_with_new_interest_dict

    total_num = 0

    pid=0

    while(1):
        results = DataAccess.get_user_with_new_interest_dict(pid,_DEBUG)

        if results==None or len(results)==0:
            break;

        if results:
            try:

                #print 'get_user_with_new_interest_dict result count:',len(results),total_num ,pid
                for result in results:
                    try:
                        #sql = " select id,frontcat,backcat,attr,attrcontent,subcat from CategoryAttr where id > "+str(id)+" order by id limit 100 ; " 
                        userid = result[0]
                        pid = userid 
                        user_with_new_interest_dict[userid ]=1

                    except:
                        print "traceback", traceback.print_exc() ,pid

            finally:
                pass


                        
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

                #print 'result count:',len(results),total_num ,pid

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
                        frontcat= frontcat.lower()

                        mappingkey=""
                        if(subsidiarycat != None and len(subsidiarycat)>1 ):
                            subsidiarycat = subsidiarycat.encode('utf-8','ignore').strip()
                            subsidiarycat = subsidiarycat.lower()
                            mappingkey="T_"+subsidiarycat 
                        elif(attributeavlue!= None and len(attributeavlue)>1 ):
                            attributeavlue= attributeavlue.encode('utf-8','ignore').strip()
                            mappingkey="K_"+attributeavlue
                            pass
                        elif(backcat != None and len(backcat)>1 ):
                            backcat= backcat.encode('utf-8','ignore').strip()
                            backcat= backcat.lower()
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


def get_project_profile_front():
    global global_project_dict_front

    total_num = 0
    pid=0

    #if(for_new_changed_data!=None):
    #    tableid=get_tableid()
    pid=0

    while(1):
        results = DataAccess.get_category_for_front(pid)
        #print 'need to rm project count',total_num 

        if results==None or len(results)==0:
            pid=0
            sleep(60*10);
            continue

        if results:
            try:
                #print 'result count:',len(results),total_num ,pid,'get_url_once_onine',for_new_changed_data
                for result in results:
                    try:
                        #sql = " SELECT pcf.id,pcf.projectid,cfd.name,pcf.categoryid FROM `mydb`.`project_category_frontend` as pcf inner join `category_frontend_def`  as cfd on pcf.categoryid =cfd.id where id > "+str(pid)+" pcf.status = 0  ORDER BY pcf.id    LIMIT 0,50;"
                        pid= result[0]
                        projectid= result[1]

                        categoryname = result[2].strip()
                        categoryname = categoryname.encode('utf-8','ignore')
                        categoryname = categoryname.lower()
                        categoryname = "f_"+categoryname

                        project_dict={}

                        if(not global_project_dict_front.has_key(projectid)):
                            #print 'profile is ',projectid,project_dict
                            global_project_dict_front[projectid]=project_dict
                        else:
                            #print 'already exist, why??',projectid
                            project_dict=global_project_dict_front[projectid]

                        total_num += 1
                        project_dict[categoryname]=1.0

                    except:
                        print "traceback", traceback.print_exc() ,pid

            finally:
                pass


                        
    #print 'project count',total_num 




def get_project_profile_increment():
    get_project_profile()

def get_project_profile(for_new_changed_data=None):
    global global_project_dict
    total_num = 0

    pid=0

    tableid=""

    if(for_new_changed_data!=None):
        tableid=get_tableid()
        #print 'gettableid------get_project_profile',tableid
    pid=0
    while(1):
        if(for_new_changed_data):
            results = DataAccess.get_url(pid,tableid)
        else:
            results = DataAccess.get_url_once_onine(pid)

        if results==None or len(results)==0:
            if(for_new_changed_data==None):
                print 'loaded all project once on line then return'
                break

            sleep(60*10);
            tableid=get_tableid()
                
            pid=0
            continue

        if results:
            try:
                #print 'result count:',len(results),total_num ,pid,'get_url_once_onine',for_new_changed_data
                for result in results:
                    try:
                        projectid= result[0]
                        pid= result[5]

#                        title = result[1].strip()
#                        #print 'default-utf[', title ,"]\n"#= result[2].strip()
#                        title = title.replace('\t',' ')
#                        title = title.replace('\n',' ')
#                        title = title.encode('utf-8','ignore')
#                        #title = title.encode('gbk','ignore')
#
#                        category = result[2].strip()
#                        #category = category.replace('\t',' ')
#                        #category = category.replace('\n',' ')
#                        category = category.encode('utf-8','ignore')
#
#                        terms = result[3].strip()
#                        terms = terms.encode('utf-8','ignore')

                        query_2_index= result[4].strip()
                        query_2_index= query_2_index.encode('utf-8','ignore')
                        #query_2_index= query_2_index.lower()
                        arr=query_2_index.strip().split("\t")

                        project_dict={}
                        if(not global_project_dict.has_key(projectid)):
                            #print 'profile is ',projectid,project_dict
                            global_project_dict[projectid]=project_dict
                        else:
                            #print 'already exist, why??',projectid
                            #for changed data, just overwrite that 
                            global_project_dict[projectid]=project_dict
                            total_num = total_num + 1

                        #print 'shouldrm33',query_2_index

                        _index=0
                        totallen=len(arr)
                        if(totallen%2!=0):
                            #print totallen,'___________not couple',projectid,'pid',pid
                            userprofilelogger.info('totallen is not couple projectid-'+str(projectid)+'-pid-'+str(pid));
                            continue

                        while _index<len(arr):
                            k=arr[_index]
                            #k=k.lower()
                            _index+=1
                            w=float(arr[_index])
                            _index+=1
                            #if(k=="T_CRM&ERP"):
                            #    print 'need to rm k--',k,projectid
                            #    os._exit(1)

                            project_dict[k]=w

                        teamgoodfeature_str = ""
                        teamgoodfeature = result[11]
                        if(teamgoodfeature ):
                            teamgoodfeature = teamgoodfeature.strip()
                            teamgoodfeature= teamgoodfeature.encode('utf-8','ignore')

                            teamgoodfeatur_dict = json.loads(teamgoodfeature)
                            for teamk1 in teamgoodfeatur_dict.keys():
                                #teamk=int(teamk1)
                                k_team="z_"+teamk1 #+"=1\t" 

                                #print 'team feature:',k_team
                                #os._exit(0)

                                project_dict[k_team]=1.0

                    except:
                        print "traceback", traceback.print_exc() ,pid

            finally:
                pass


                        
    #print 'project count',total_num 


def get_user_profile(u,current_mode): #,current_u):
    return redis_get_user_profile(u,current_mode)

#    k=str(u)
#    if(current_mode==_WEEKLY):
#        k+="_WEEK"
#
#    udict = None
#    r = redis.Redis(host='127.0.0.1', port=6379, db=0)   #如果设置了密码，就加上password=密码
#    uprofile_json=r.get(k)   
#    if(uprofile_json!= None):
#        udict = json.loads(uprofile_json)
#    return udict 
#

def merge_with_old(current_u,old_userprofile,current_mode,_total_key_dict_,new_dict):
    for _type,type_dict in old_userprofile.items():

        new_type_dict={}
        if(new_dict.has_key(_type)):
            new_type_dict=new_dict[_type]
        else:
            new_dict[_type]=new_type_dict

            
        for k,v1 in type_dict.items():


            #if(k=="T_CRM&ERP"):
            #    print 'need 2222--merge_with_old--to rm k--',k
            #    os._exit(1)

            _total_key_dict_[k]=1
            v=v1
            #if(v<0.0):
            #    print 'merge 1 less_than_zero'
            #    raw_input()
            if(current_mode!=_REALTIME):
                v=v*DECREMENT_STEP

            if(current_u.has_key(k)):

                v_new=current_u[k]
                if(current_mode!=_REALTIME):
                    v+=v_new
                else:
                   #for realtime mode
                   v+=v_new*1.2

            new_type_dict[k]=v

    #no use to return ,since call by object(mutable)
    #return _total_key_dict_,new_dict



def merge(current_u,old_userprofile,old_userprofile_front,current_mode):
    new_dict={}
    new_dict_front={}


#    print 'need to rm'
#    s1= json.dumps(current_u)
#    s2= json.dumps(old_userprofile)
#    print 'need to rm end'


    #just use it to record all the keys
    _total_key_dict_={}
    #print 'old_userprofile,old_userprofile_front',len(old_userprofile.keys()),len(old_userprofile_front.keys())
    merge_with_old(current_u,old_userprofile,current_mode,_total_key_dict_,new_dict)
    #len_up=len(old_userprofile.keys())
    #len_keys=len(_total_key_dict_.keys())
    merge_with_old(current_u,old_userprofile_front,current_mode,_total_key_dict_,new_dict_front)

#    testk="f_电商"
#    if(new_dict_front.has_key("f_")):
#        if(new_dict_front["f_"].has_key(testk)):
#            print 'testk',testk,new_dict_front["f_"][testk]
#        aa=new_dict_front["f_"]
#        for k,v in  aa.items():
#            print "["+k+"]",len(k),v


    #if(len(new_dict_front.keys())>0):
    #    print 'need2rm in merge',len(new_dict_front["f_"].keys())

    #len_up_front=len(old_userprofile_front.keys())
    #len_keys_front=len(_total_key_dict_.keys())
    #if(len_keys!=len_keys_front):
    #    print 'len_keys!=len_keys_front',len_keys,len_keys_front
        
#    if(len(old_userprofile_front.keys())>0 and len_keys==len_keys_front):
#        print 'len_keys!=len_keys_front',len_keys,len_keys_front,len(old_userprofile_front.keys())
#        print 'error'
#        for k1,v1 in old_userprofile_front.items():
#            print 'front-----',k1,len(v1.items())
#        os._exit(0)
#
    #print 'after front debug verify whether total_key_dict has changed',len(_total_key_dict_.keys())

#    #for k,v1 in old_userprofile.items():
#    for _type,type_dict in old_userprofile.items():
#
#        new_type_dict={}
#        if(new_dict.has_key(_type)):
#            new_type_dict=new_dict[_type]
#        else:
#            new_dict[_type]=new_type_dict
#
#            
#        for k,v1 in type_dict.items():
#            _total_key_dict_[k]=1
#            v=v1
#            #if(v<0.0):
#            #    print 'merge 1 less_than_zero'
#            #    raw_input()
#            if(current_mode!=_REALTIME):
#                v=v*0.8
#
#            if(current_u.has_key(k)):
#
#                v_new=current_u[k]
#                if(current_mode!=_REALTIME):
#                    v+=v_new
#                else:
#                   #for realtime mode
#                   v+=v_new*1.2
#
#            new_type_dict[k]=v
#            
#    print 'debug verify whether total_key_dict has changed',len(_total_key_dict_.keys()

    for k,v1 in current_u.items():

        #if(k=="T_CRM&ERP"):
        #    print 'need 2k,v1 in current_u.it3333--to rm k--',k
        #    os._exit(1)

        #if(old_userprofile.has_key(k)):
        if(_total_key_dict_.has_key(k)):
            continue

        v=v1

#        if(v<0.0):
#            print 'merge 2 less_than_zero',k,v
#            raw_input()

        if(current_mode==_REALTIME):
            v=v*1.2

        _type=""

        if(k.startswith("f_")):
            _type="f_"

            new_type_dict_front={}
            if(new_dict_front.has_key(_type)):
                new_type_dict_front=new_dict_front[_type]
            else:
                new_dict_front[_type]=new_type_dict_front

            new_type_dict_front[k]=v

        else:
            if(k.startswith("T_")):
                _type="T_"
            elif(k.startswith("t_")):
                _type="t_"
            elif(k.startswith("K_")):
                _type="K_"
            elif(k.startswith("z_")):
                _type="z_"
            else:
                _type="k_"
                
            new_type_dict={}
            if(new_dict.has_key(_type)):
                new_type_dict=new_dict[_type]
            else:
                new_dict[_type]=new_type_dict

            new_type_dict[k]=v




#    print 'need to rm'
#    s3= json.dumps(new_dict)
#    print 's1',s1
#    print 's2',s2
#    print 's3',s3
#    print 'need to rm end'
#
    return new_dict,new_dict_front



MAX_F_count=100
MAX_T_count=100
MAX_K_count=200
MAX_z_count=200
MAX_t_count=200
MAX_k_count=500

def update_user_profile_by_type(u,current_u,current_mode,isfront):

    #topfeatures= sorted(current_u.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)#[0:1000]
    T_count=0
    K_count=0
    t_count=0
    k_count=0
    z_count=0
    f_count=0

    T_dict={}
    t_dict={}
    K_dict={}
    k_dict={}
    z_dict={}
    f_dict={}
    
    for typeid,type_dict in current_u.items():
        #print 'typeid:',typeid,type_dict,type(type_dict )
        #raw_input()
        #exit()

        topfeatures= sorted(type_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)#[0:1000]

        for k_v in topfeatures:
            k=k_v[0]
            v=k_v[1]
            if(v<0):
                #print k,v,'less than 0'
                #raw_input()
                continue


            if(k.startswith("f_")):
                f_count +=1
                if(f_count>MAX_F_count):
                    continue
                f_dict[k]=v

            elif(k.startswith("T_")):
                T_count +=1
                if(T_count>MAX_T_count):
                    continue
                T_dict[k]=v
            elif(k.startswith("t_")):
                t_count +=1
                if(t_count>MAX_t_count):
                    continue
                t_dict[k]=v
            elif(k.startswith("K_")):
                K_count +=1
                if(K_count>MAX_K_count):
                    continue
                K_dict[k]=v

            elif(k.startswith("z_")):
                #print 'z____----------------------',k
                #print 'need to rm'
                #os._exit(0)

                z_count +=1
                if(z_count >MAX_z_count):
                    continue
                z_dict[k]=v

            else:
                k_count +=1
                if(k_count>MAX_k_count):
                    continue
                k_dict[k]=v

    u_profile_dict_by_cate={}
    userk=str(u)
    with_front_interest=0
    if(isfront==1):
        if(len(f_dict.keys())):
            u_profile_dict_by_cate["f_"]=f_dict
            userk+="_FRONT"
            with_front_interest=1

            uprofilestr= json.dumps(u_profile_dict_by_cate)
            redis_update_user_profile(userk,uprofilestr,current_mode)
    else:
        u_profile_dict_by_cate["T_"]=T_dict
        u_profile_dict_by_cate["t_"]=t_dict
        u_profile_dict_by_cate["K_"]=K_dict
        u_profile_dict_by_cate["k_"]=k_dict
        u_profile_dict_by_cate["z_"]=z_dict

        uprofilestr= json.dumps(u_profile_dict_by_cate)
        redis_update_user_profile(userk,uprofilestr,current_mode)

    return


def update_user_profile(u,current_u,current_u_front,current_mode):
    isfront=0
    update_user_profile_by_type(u,current_u,current_mode,isfront)
    isfront=1
    update_user_profile_by_type(u,current_u_front,current_mode,isfront)

#    #topfeatures= sorted(current_u.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)#[0:1000]
#    T_count=0
#    K_count=0
#    t_count=0
#    k_count=0
#    z_count=0
#
#    T_dict={}
#    t_dict={}
#    K_dict={}
#    k_dict={}
#    z_dict={}
#    
#    for typeid,type_dict in current_u.items():
#        #print 'typeid:',typeid,type_dict,type(type_dict )
#        #raw_input()
#        #exit()
#
#        topfeatures= sorted(type_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)#[0:1000]
#
#        for k_v in topfeatures:
#            k=k_v[0]
#            v=k_v[1]
#            if(v<0):
#                #print k,v,'less than 0'
#                #raw_input()
#                continue
#            if(k.startswith("T_")):
#                T_count +=1
#                if(T_count>MAX_T_count):
#                    continue
#                T_dict[k]=v
#            elif(k.startswith("t_")):
#                t_count +=1
#                if(t_count>MAX_t_count):
#                    continue
#                t_dict[k]=v
#            elif(k.startswith("K_")):
#                K_count +=1
#                if(K_count>MAX_K_count):
#                    continue
#                K_dict[k]=v
#
#            elif(k.startswith("z_")):
#                #print 'z____----------------------',k
#                #print 'need to rm'
#                #os._exit(0)
#
#                z_count +=1
#                if(z_count >MAX_z_count):
#                    continue
#                z_dict[k]=v
#
#            else:
#                k_count +=1
#                if(k_count>MAX_k_count):
#                    continue
#                k_dict[k]=v
#
#    u_profile_dict_by_cate={}
#    u_profile_dict_by_cate["T_"]=T_dict
#    u_profile_dict_by_cate["t_"]=t_dict
#    u_profile_dict_by_cate["K_"]=K_dict
#    u_profile_dict_by_cate["k_"]=k_dict
#    u_profile_dict_by_cate["z_"]=z_dict
#
#    uprofilestr= json.dumps(u_profile_dict_by_cate) #current_u)
#
#    redis_update_user_profile(u,uprofilestr,current_mode)

#    r = redis.Redis(host='127.0.0.1', port=6379, db=0)   #如果设置了密码，就加上password=密码
#    #need-update-
#    k=str(u)
#    #k=str(u)+"_newprofile"
#    r.set(k,uprofilestr)
#
#    if(current_mode==_WEEKLY):
#        #need-update-
#        k+="_WEEK"
#        #k+="_WEEK_newprofile"
#        r.set(k,uprofilestr)
#    


#    rslt=r.get(k)   
#
#    print 'key is;',k
#    print 'press any key'
#    raw_input()
#
#    print rslt

    return




#    adict={}
#    alist=[1,2,3]
#    alist2=[7,8,9]
#    blist=[alist,alist2]
#
#    adict["k1"]=blist
#
#    r.set('tt', adict)  
#    rslt=r.get('tt')   
#    #print rslt
#
#
#    #print rslt
#    sys.exit()


TOTAL_USER_COUNT=8500.0


def update_single_userprofile(userprofile_dict_current,projectid,u,behaviortype,createtime,bweight,iuf,isfront):
    #begin_of_week_timestamp,user_tract_dict,_project_profile_dict,current_mode):
    global global_project_dict
    global global_project_dict_front

    project_dict=None
    if(isfront):
        if(global_project_dict_front.has_key(projectid)):
            project_dict=global_project_dict_front[projectid]
            #print 'project_dict=global_project_dict_front[projectid]','update_single_userprofile',len(project_dict.keys()),projectid
    else:
        if(global_project_dict.has_key(projectid)):
            project_dict=global_project_dict[projectid]

    if(project_dict!=None):
        current_u=defaultdict(float)

        if(userprofile_dict_current.has_key(u)):
            current_u=userprofile_dict_current[u]
        else:
            userprofile_dict_current[u]=current_u

        need_team=0
        if(team_interest_behavior.has_key(behaviortype)):
            need_team=1

        for k,v1 in project_dict.items():

            if(isfront==None or isfront==0):
                #team feature is starts with z_
                if(k.startswith("z_")):
                    if(need_team==0):
                        continue

            v=v1*bweight*iuf

            #if(k=="T_CRM&ERP"):
            #    print 'need 2222--update--to rm k--',k,projectid
            #    os._exit(1)

            #if(isfront):
            #    print 'need2rmjudget whether forntend cate',k

            if(current_u.has_key(k)):
                #old data,just add them,without decay
                if(createtime<1425073577  ):
                    current_u[k]=v+current_u[k]
                else:
                    current_u[k]=v+current_u[k]
#                            if(current_mode==_REALTIME):
#                                current_u[k]=v*1.2+current_u[k]
#                            else:
#                                current_u[k]=v+current_u[k]*.088
            else:
                current_u[k]=v



WEEK_TOTAL_SECONDS=3600*24*7

#u_dict={}
def weekly_data_porcess(begin_of_week_timestamp,user_tract_dict,_project_profile_dict,current_mode):
    global global_project_dict
    #global u_dict
    userprofile_dict_current={}


    #updated_u=defaultdict(int)
    for u,tracks in user_tract_dict.items():
        for p_type_time in tracks:
            #print "p_type_time:",  p_type_time 
            #p_type_time=[projectid,behaviortype,createtime]
            projectid=p_type_time[0]

            behaviortype=p_type_time[1]
            createtime=p_type_time[2]
            if(not behavior_weight.has_key(behaviortype)):
                continue

            bweight=behavior_weight[behaviortype]
            if(bweight<=0.1):
                continue

            #print 'bweight',bweight
            #if(u==25150): 
            #    print 'press ayn key need to rm 25150',bweight,projectid,createtime
            #    raw_input()

            if(projectid==0):
                k=p_type_time[3]

                #if(k.startswith("f_")):
                #    print 'need 2 rm',k

                if(1): #not k.startswith("f_")):
                    #print "projectid==0):",bweight,k

                    #only filter match this condition
                    if(behaviortype!="filter_label__##"):
                        print 'project is o and type is not filter',behaviortype
                        continue

                    timestamp_now=int(time.time())
                    seconds_elapse=timestamp_now-createtime
                    decrement_volumn=1.0

                    week_eplase=int(seconds_elapse/WEEK_TOTAL_SECONDS)
                    if(week_eplase>1):
                        decrement_volumn=DECREMENT_STEP**week_eplase

                        #if(u==25150): 
                        #    print '-------------should rm press any key DECREMENT_STEP',decrement_volumn,DECREMENT_STEP,week_eplase,WEEK_TOTAL_SECONDS,bweight,behaviortype
                        #    print 'press ayn key need to rm 25150',bweight,projectid,createtime
                        #    raw_input()

                    v=bweight*decrement_volumn
                    #print 'press ayn key need to rm 25150',bweight,projectid,createtime,"v=",v,'k=',"["+k+"]",len(k)

                    current_u=defaultdict(float)

                    if(userprofile_dict_current.has_key(u)):
                        current_u=userprofile_dict_current[u]
                    else:
                        userprofile_dict_current[u]=current_u

                    if(current_u.has_key(k)):
                        current_u[k]=v+current_u[k]
                    else:
                        current_u[k]=v
                else:
                    #print '--front interest--'
                    pass

            else:

                _p_profile=None
                iuf=1.0

                #_project_profile_dict viewcount,bp_viewcount,meeting etc
                if(_project_profile_dict.has_key(projectid)):
                    _p_profile=_project_profile_dict[projectid]

                    total_action_count=_p_profile.viewcount+_p_profile.bp_viewed_count+_p_profile.marked_count+_p_profile.like_count+_p_profile.apply_meeting_count+ _p_profile.replied_count              

                    #iuf=TOTAL_USER_COUNT/(_p_profile.viewcount+1.0)
                    iuf=TOTAL_USER_COUNT/(total_action_count+1.0)
                    if(iuf>1.0):
                        iuf=1.0

                    #raw_input()

                    iuf=math.log(iuf)
                    
                    if(iuf<0.2):
                        #print 'iuf less than zero',iuf,_p_profile.viewcount,TOTAL_USER_COUNTOTAL_USER_COUNT
                        iuf=0.2
                    elif(iuf>3.5):
                        iuf=3.5

                    #raw_input()

                #userprofile_dict_current is by reference
                isfront=0
                update_single_userprofile(userprofile_dict_current,projectid,u,behaviortype,createtime,bweight,iuf,isfront)
                isfront=1
                update_single_userprofile(userprofile_dict_current,projectid,u,behaviortype,createtime,bweight,iuf,isfront)

                #category,tag,term weight of one project
#                if(global_project_dict.has_key(projectid)):
#                    #use it for iteratoring later
#                    #updated_u[u]=1
#                    project_dict=global_project_dict[projectid]
#
#                    current_u=defaultdict(float)
#
#                    if(userprofile_dict_current.has_key(u)):
#                        current_u=userprofile_dict_current[u]
#                    else:
#                        userprofile_dict_current[u]=current_u
#
#    #                if(u_dict.has_key(u)):
#    #                    current_u=u_dict[u]
#    #                else:
#    #                    u_dict[u]=current_u
#    #
#                            
#                    need_team=0
#                    if(team_interest_behavior.has_key(behaviortype)):
#                        need_team=1
#
#                    for k,v1 in project_dict.items():
#                        #print 'iuf',iuf,v1,bweight
#                        #raw_input()
#
#                        #team feature is starts with z_
#                        if(k.startswith("z_")):
#                            if(need_team==0):
#                                continue
#
#                        v=v1*bweight*iuf
#                        #print 'weight',v,v1,bweight,behaviortype
#
#                        if(current_u.has_key(k)):
#                            #old data,just add them,without decay
#                            if(createtime<1425073577  ):
#                                current_u[k]=v+current_u[k]
#                            else:
#                                current_u[k]=v+current_u[k]
#    #                            if(current_mode==_REALTIME):
#    #                                current_u[k]=v*1.2+current_u[k]
#    #                            else:
#    #                                current_u[k]=v+current_u[k]*.088
#                        else:
#                            current_u[k]=v
#
#                else:
#                    pass
#                    #print 'not has this key,why??',projectid,len(global_project_dict.items())
                    #os._exit(0)

    for u in userprofile_dict_current.keys():
        #if(not u_dict.has_key(u)):
        #    #print 'user not existed',u
        #    continue
        #    #os._exit(0)
        current_u=userprofile_dict_current[u]
        old_userprofile=get_user_profile(u,current_mode)
        if(old_userprofile==None):
            old_userprofile={} 


        front_userk=str(u)+"_FRONT"
        old_userprofile_front=redis_get_user_profile_frontend(front_userk,current_mode)
        if(old_userprofile_front==None):
            old_userprofile_front={}


        #if(u==25150): 
        #    print 'press ayn key need to rm 25150',len(current_u.keys()),len(old_userprofile_front.keys()),len(old_userprofile.keys())
        #    raw_input()


        #current_u=merge(current_u,old_userprofile,current_mode)
        new_u_profile_dict,new_u_profile_dict_front=merge(current_u,old_userprofile,old_userprofile_front,current_mode)
        #print "new_u_profile_dict,new_u_profile_dict_front",len(new_u_profile_dict),len(new_u_profile_dict_front)

        try:
            update_user_profile(u,new_u_profile_dict,new_u_profile_dict_front,current_mode)
        except:
            errorstr='update_user_profile-'+ traceback.print_exc()
            userprofilelogger.info(errorstr)

        #print 'after update userprofile \n press any key'
        #raw_input()
        pass

    #if(current_mode==_HISTORY): #REALTIME):
    #    update_project_stat_info(_project_profile_dict)
    #    pass







def update_project_stat_info(pid,_project_profile): #_project_profile_dict):
    #print len(_project_profile_dict.items()),'len of _project_profile_dict'
    #for pid,_project_profile in _project_profile_dict.items():

    DataAccess.update_project_stat_info(pid,
        _project_profile.viewcount,
        #_project_profile.updatetime,
        _project_profile.bp_viewed_count,
        _project_profile.apply_meeting_count,
        _project_profile.replied_count,
        _project_profile.marked_count,
        _project_profile.exposed_count,
        _project_profile.like_count,_DEBUG)


def update_project_stat_info_HISTORY(_project_profile_dict):
    #print '-----------------------update_project_stat_info_HISTORY',time.strftime("%Y-%m-%d %H:%M:%S"),len(_project_profile_dict.items()),'len of _project_profile_dict'
    for pid,_project_profile in _project_profile_dict.items():
        update_project_stat_info(pid,_project_profile)

    #print 'end-----------------------update_project_stat_info_HISTORY',time.strftime("%Y-%m-%d %H:%M:%S")
    #print 'should remove,press any key'
    #raw_input()
    

#        DataAccess.update_project_stat_info(pid,
#            _project_profile.viewcount,
#            #_project_profile.updatetime,
#            _project_profile.bp_viewed_count,
#            _project_profile.apply_meeting_count,
#            _project_profile.replied_count,
#            _project_profile.marked_count,
#            _project_profile.exposed_count)
#
        
first_round_file='__user_profile_first_round_'+_DEBUG

def get_event_track_totalcount():
    global first_round_file

    totalcount=0

    if not os.path.exists(first_round_file):
        totalcount=100*10000
    else:
        os.remove(first_round_file)

    return totalcount


def get_project_stat_info(pid):
#    viewcount =0
#    bp_viewed_count=0
#    apply_meeting_count =0
#    replied_count=0
#    marked_count=0
#    exposed_count=0

    results = DataAccess.get_project_stat_info(pid,_DEBUG)
    _project_profile=p_profile()

    if results and len(results)>0:
        try:
            for result in results:
                viewcount = result[0]
                bp_viewed_count = result[1]
                apply_meeting_count = result[2]
                replied_count = result[3]
                marked_count = result[4]
                exposed_count  = result[5]
                like_count  = result[6]

                if(viewcount==None):
                    viewcount =0
                if(bp_viewed_count ==None):
                    bp_viewed_count = 0
                if(apply_meeting_count ==None):
                    apply_meeting_count =0
                if(replied_count ==None):
                    replied_count = 0
                if(marked_count ==None):
                    marked_count =0
                if(exposed_count  ==None):
                    exposed_count  = 0
                if(like_count  ==None):
                    like_count  = 0


                _project_profile.viewcount=viewcount
                #_project_profile.updatetime=updatetime
                _project_profile.bp_viewed_count=bp_viewed_count
                _project_profile.apply_meeting_count=apply_meeting_count
                _project_profile.replied_count=replied_count
                _project_profile.marked_count=marked_count
                _project_profile.exposed_count=exposed_count
                _project_profile.like_count  =like_count  
                _project_profile.recommend_count =0 

                break
        except:
            print 'err in get_project_stat'
    return _project_profile
    #viewcount , bp_viewed_count , apply_meeting_count , replied_count , marked_count , exposed_count


#@profile
def business_contrl(request_mode=None):
    global front_back_mapping
    global user_with_new_interest_dict

    _project_profile_dict={}

    #only used in history mode
    user_project_exposed_view={}

    eventid=0
    #eventid_new_interest=109000
    eventid_new_interest=0

    eventid_filter_label=0

    #curtimestamp=time.time()
    begin_of_week_timestamp=0 #curtimestamp-3600*24
    end_of_thisweek_timestamp=0 #curtimestamp-3600*24
    #p_type_time=[projectid,behaviortype,createtime]

    timestamp_now=int(time.time())
    date_time_now=time.localtime(timestamp_now)
    tmy_now=date_time_now.tm_year
    tmm_now=date_time_now.tm_mon
    tmd_now=date_time_now.tm_mday

    tmw_now=date_time_now.tm_wday
    _begin_of_thisday_now=datetime.datetime(tmy_now,tmm_now,tmd_now)

    #print 'zero_of_thisday', zero_of_thisday
    #timeArray_end_now = time.strptime(str(_begin_of_thisday_now) , "%Y-%m-%d %H:%M:%S")        
    #zero_timeStamp_now = int(time.mktime(timeArray_end_now ))    


    dtt_end_now = _begin_of_thisday_now.timetuple() 
    zero_timeStamp_now = time.mktime(dtt_end_now ) # 1293868800.0

    end_of_thisweek_timestamp_now = zero_timeStamp_now + (7-tmw_now)*24*3600 #-1
    begin_of_thisweek_timestamp_now = end_of_thisweek_timestamp_now -7*24*3600 #-1
    print 'begin_of_thisweek_timestamp_now',begin_of_thisweek_timestamp_now ,'end_of_thisweek_timestamp_now ', end_of_thisweek_timestamp_now 

    end_of_thisweek_timestamp_lastweek=zero_timeStamp_now + (7-tmw_now)*24*3600-7*24*3600

    userprofilelogger.info('-weekly----------eventid-'+str(eventid)+"-eventid_new_interest-"+str(eventid_new_interest)+"--eventid_filter_label-"+str(eventid_filter_label)+"-")

    #end_of_thisweek_timestamp_now = zero_timeStamp_now + (7-tmw_now)*24*3600-7*24*3600

    #print begin_of_thisweek_timestamp_now ,"_begin_of_thisday_now",_begin_of_thisday_now
    #raw_input()
    #end_date_time_=time.localtime(end_of_thisweek_timestamp_now )

    user_tract_dict=defaultdict(list)

    #1 for history; 2:realtime;3:weekly  should begin with history->realtime->weekly-->realtime_weekly (then iterator like this)
    #default is history mode
    current_mode=_HISTORY
    if(request_mode!=None):
        current_mode=request_mode
        
    last_updated_eventid=0
    last_maxid_in_lastweek="./lastid_max_eventid_last_week"+_DEBUG
    last_projectid_file="./lastid_record_eventid"+_DEBUG

    last_maxid_in_lastweek_new_interest="./lastid_max_eventid_last_week_new_interest"+_DEBUG
    last_projectid_file_new_interest="./lastid_record_eventid_new_interest"+_DEBUG

    last_maxid_in_lastweek_for_label="./lastid_max_eventid_last_week_for_label"+_DEBUG
    last_projectid_file_for_label="./lastid_record_eventid_for_label"+_DEBUG

    lastmaxid=0

    if(current_mode==_WEEKLY):

        eventid=getlastid(last_maxid_in_lastweek)
        eventid_new_interest=getlastid(last_maxid_in_lastweek_new_interest)
        eventid_filter_label=getlastid(last_maxid_in_lastweek_for_label)

        userprofilelogger.info('-weekly----------eventid-'+str(eventid)+"-eventid_new_interest-"+str(eventid_new_interest)+"--eventid_filter_label-"+str(eventid_filter_label)+"-")

    else:
        eventid=getlastid(last_projectid_file)
        eventid_new_interest=getlastid(last_projectid_file_new_interest)
        eventid_filter_label=getlastid(last_projectid_file_for_label)

        userprofilelogger.info('--eventid-'+str(eventid)+"-eventid_new_interest-"+str(eventid_new_interest)+"--eventid_filter_label-"+str(eventid_filter_label)+"-")


#    userprofilelogger.info('--should rm--------idmodify')
#    print '--should rm--------idmodify'
#    if(eventid<200*10000):
#        eventid=240*10000
#    if(eventid_new_interest<200*10000):
#        eventid_new_interest=200*10000



#    #---------------------end of update user-project-behavior-track

    total_user_track_count=get_event_track_totalcount()
    userprofilelogger.info('--total_user_track_count:'+str(total_user_track_count))

    addcount = 0 

    u_p_dict={}

    switch_interest_new=0

    iteratorindex=0

    while(1):
        #iteratorindex+=1
        #if(iteratorindex>10):
        #    print 'need to rm'
        #    os._exit(0)

        if(current_mode==_REALTIME):
            realtime_timestamp=int(time.time())
            #print 'should rm_endofweek  replace with upper line; '
            #userprofilelogger.info('-should rm this code endofweek')
            #if(realtime_timestamp>(end_of_thisweek_timestamp_now-7*24*3600)):
            if(realtime_timestamp>end_of_thisweek_timestamp_now):
                userprofilelogger.info('--end of realtime')
                #print 'exit for weekly mode'
                #exit()
                #change from realtime to weekly
                return _REALTIME

        results = None

        #need to update for user_label,only the real mode use the filter action
        #for realtime mode,just switch among 0,1,2; 0: for event; 1 for filter label; 2 for app_log
        if(current_mode==_REALTIME or current_mode==_WEEKLY):

            switch_interest_new+=1
            switch_interest_new = switch_interest_new % 3
            #print 'switch_interest_new',switch_interest_new,'eventid_filter_label',eventid_filter_label

#            if(switch_interest_new==1):
#                switch_interest_new=2
#            elif(switch_interest_new==2):
#                switch_interest_new=0
#            elif(switch_interest_new==0):
#                switch_interest_new=1

        elif(current_mode==_HISTORY):
            #for history mode,just switch among 0,2; 0: for event; 2 for app_log
            if(switch_interest_new==2):
                switch_interest_new=0
            elif(switch_interest_new==0):
                switch_interest_new=2
                
        if(switch_interest_new==1):
            results = DataAccess.get_event_user_label_filtered(eventid_filter_label)
        elif(switch_interest_new==2):
            results = DataAccess.get_event_track_new_interest(eventid_new_interest)
        else:
            results = DataAccess.get_event_track(eventid)

        if results==None  or len(results)==0:
            if(switch_interest_new == 0 and current_mode==_WEEKLY):
                #no data,just update weekly user profile,it's time when this week ends 
                #print '1 weekly_data_porcess',eventid
                weekly_data_porcess(begin_of_week_timestamp,user_tract_dict,_project_profile_dict,current_mode)

                writefile4int(last_maxid_in_lastweek,eventid)
                writefile4int(last_maxid_in_lastweek_new_interest,eventid_new_interest)
                writefile4int(last_maxid_in_lastweek_for_label,eventid_filter_label)
                userprofilelogger.info('--end of weekly for no result')

                #after the weekly data process, the user_track_dict should be vanished
                user_tract_dict=defaultdict(list)
                addcount =0
                #change from weekly to history(to realtime)
                return _WEEKLY

            #last_updated_eventid=eventid

            #print 'no result business control',eventid ,'curmode',current_mode #last_updated_eventid
            if(current_mode!=_WEEKLY):
                sleep(1);
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
                        _eventid= result[0]

                        if( switch_interest_new==1):
                            eventid_filter_label=_eventid
                        elif( switch_interest_new==2):
                            eventid_new_interest=_eventid
                        else:
                            eventid=_eventid

                        userid= result[1]

                        #sql = "SELECT labelid,userid,type,label FROM `mydb`.`user_label` where labelId > "+str(logid+"  ORDER BY labelId  limit 500;"

                        #only the _REALTIME mode use this mode ; for realtime mode,just process data one by one
                        if(switch_interest_new==1):
                            if(current_mode==_REALTIME):
                                createtime = result[3]
                                keyword = result[4]

                                #print 'rm later',_eventid,keyword,len(keyword)
                                keyword = keyword.encode('utf-8','ignore')
                                keyword = keyword.lower()

                                if(keyword):

                                    dtt = createtime.timetuple() 
                                    current_timeStamp = time.mktime(dtt)

                                    keyword_front = "f_"+keyword
                                    behaviortype="filter_label__##"
                                    p_type_time=[0,behaviortype,current_timeStamp,keyword_front]
                                    user_tract_dict[userid].append(p_type_time)

                                    if(front_back_mapping.has_key(keyword)):
                                        #for backend category
                                        #dtt = createtime.timetuple() 
                                        #current_timeStamp = time.mktime(dtt)

                                        back_keys_dict=front_back_mapping[keyword]
                                        #print len(back_keys_dict.keys()),keyword
                                        for keyword in back_keys_dict.keys():
                                            p_type_time=[0,behaviortype,current_timeStamp,keyword ]
                                            user_tract_dict[userid].append(p_type_time)

                                    #for frontend category

                                    weekly_data_porcess(begin_of_week_timestamp,user_tract_dict,_project_profile_dict,current_mode)
                                    #after the weekly data process, the user_track_dict should be vanished
                                    user_tract_dict=defaultdict(list)

                                writefile4int(last_projectid_file_for_label,eventid_filter_label)

                            #after processing the user label's data,just continue
                            continue

                        projectid= result[2]
                        if(projectid<0):
                            continue
                        behaviortype= result[3]
                        #print 'behaviortype', behaviortype,_eventid,projectid

                        if(not behaviortype):
                            continue

                        behaviortype= behaviortype.encode('utf-8','ignore')
                        behaviortype=behaviortype.lower().strip()

                        createtime = result[4]

                        subtype=""
                        filterinterest_for_new=""

                        if(switch_interest_new==1):
                            #since we've already continue upword, so this section won't run at all
                            userprofilelogger.info('--eventid_filter_label-'+str(eventid_filter_label)+"-should not run at here")

                            #sql = " SELECT logid,userid,objectid,type,creationtime,subtype,strvalue2 FROM `mydb`.`investor_app_log` where logid > "+str(logid)+" ORDER BY `logId` LIMIT 0,500;"
                            subtype= result[5]
                            filterinterest_for_new= result[6]
                            if(subtype):
                                subtype= subtype.encode('utf-8','ignore')
                                subtype= subtype.lower()
                            else:
                                subtype=""

                            if(filterinterest_for_new):
                                filterinterest_for_new= filterinterest_for_new.encode('utf-8','ignore').strip()
                                filterinterest_for_new= filterinterest_for_new.lower()
                            else:
                                filterinterest_for_new=""

                        elif(switch_interest_new==2):
                            #sql = " SELECT logid,userid,objectid,type,creationtime,subtype,strvalue2 FROM `mydb`.`investor_app_log` where logid > "+str(logid)+" ORDER BY `logId` LIMIT 0,500;"
                            subtype= result[5]
                            isfirst = result[7]
                            if(isfirst != 1):
                                continue

                            if(subtype):
                                subtype= subtype.encode('utf-8','ignore')
                                subtype= subtype.lower().strip()
                            else:
                                subtype=""


                        if(eventid%30001==10001 or eventid_new_interest % 30001==10001 or (eventid%3001==1001 and current_mode==_REALTIME)):
                            #print '--eventid',eventid,time.strftime("%Y-%m-%d %H:%M:%S")        
                            userprofilelogger.info('--eventid-'+str(eventid)+"-eventid_filter_label="+str(eventid_filter_label)+"==eventid_new_interest:"+str(eventid_new_interest)+"--"+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"_switch_interest_new:"+str(switch_interest_new))

                        #print 'need2rm',createtime 

                        dtt = createtime.timetuple() 
                        current_timeStamp = time.mktime(dtt) # 1293868800.0

                        #print 'need2rm',(current_mode==_HISTORY and (current_timeStamp>begin_of_thisweek_timestamp_now  and current_timeStamp < end_of_thisweek_timestamp_now ))
                        #print current_mode,_HISTORY ,current_timeStamp,begin_of_thisweek_timestamp_now , end_of_thisweek_timestamp_now 

                        #if the time period is within this week,just switch to realtime mode
                        if(current_mode==_HISTORY and switch_interest_new == 0 and (current_timeStamp>begin_of_thisweek_timestamp_now  and current_timeStamp < end_of_thisweek_timestamp_now )):
                            userprofilelogger.info("begin batch switch_interest_new="+str(switch_interest_new)+" current_mode="+str(current_mode)+" current_timeStamp="+str(current_timeStamp) + " begin_of_thisweek_timestamp_now "+str(begin_of_thisweek_timestamp_now)+" end_of_thisweek_timestamp_now "+str(end_of_thisweek_timestamp_now ))
                            userprofilelogger.info('--eventid-'+str(eventid)+"-eventid_filter_label="+str(eventid_filter_label)+" eventid_new_interest:"+str(eventid_new_interest)+"--"+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"_switch_interest_new:"+str(switch_interest_new))

                            update_project_stat_info_HISTORY(_project_profile_dict)
                            current_mode=_REALTIME
                            
                            if(total_user_track_count<50*10000):
                                userprofilelogger.info('-----------------------batch add_user_track_record begin--'+str(time.strftime("%Y-%m-%d %H:%M:%S")))
                                updatecount=0
                                bulk_str=""
                                for _userid,_project_e_v_dict in user_project_exposed_view.items():
                                    for _projectid,_e_v in _project_e_v_dict.items():

                                        #bulk_str+="("+str(_projectid)+","+str(_userid)+","+str(_e_v[1])+","+str(_e_v[0])+"),"
                                        bulk_str+="(%d,%d,%d,%d)," % (_projectid,_userid,_e_v[1],_e_v[0])
                                        #"+str(_projectid)+","+str(_userid)+","+str(_e_v[1])+","+str(_e_v[0])+"),"
                                        #print bulk_str
                                        updatecount+=1

                                        #if(0): #updatecount%1111==1001):
                                        if(updatecount%1111==1001):
                                            bulk_str=bulk_str.strip(',')
                                            DataAccess.bulk_add_user_track_record(bulk_str,_DEBUG)
                                            #add_user_track_record (_projectid,_userid,_e_v[1],_e_v[0])
                                            bulk_str=""
                                        #sql ="insert into user_track_record (projectid,userid,viewcount,exposedcount) values %s;" % (bulk_str)

                                if(len(bulk_str)>0):
                                    bulk_str=bulk_str.strip(',')
                                    DataAccess.bulk_add_user_track_record(bulk_str,_DEBUG)
                                    bulk_str=""
                                    #print '111122222 rm'
                                    #os._exit(1)

                                user_project_exposed_view={}
                                userprofilelogger.info('-----------------------batch add_user_track_record --'+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"__"+str(updatecount))
                            #---------------------end of update user-project-behavior-track

                        if(switch_interest_new>0):
                            if(not user_with_new_interest_dict.has_key(userid)):
                                DataAccess.add_user_with_new_interest_dict(userid,_DEBUG)
                                user_with_new_interest_dict[userid]=1

                            behaviortype+="##"
                            if(not behavior_weight.has_key(behaviortype)):
                                behaviortype+=subtype
                                if(not behavior_weight.has_key(behaviortype)):
                                    continue
                                else:
                                    pass
                            else:
                                pass

                        else:
                            if(not behavior_weight.has_key(behaviortype)):
                                continue

                        _project_profile=None
                        if(_project_profile_dict.has_key(projectid)):
                            _project_profile=_project_profile_dict[projectid]
                        else:
                            _project_profile=get_project_stat_info(projectid)
                            _project_profile.projectid=projectid
                            _project_profile_dict[projectid]=_project_profile

                        if(behaviortype=="viewed" or behaviortype.startswith("project_view") ):
                            _project_profile.viewcount+=1
                        elif(behaviortype.startswith("bp_viewed")):
                            _project_profile.bp_viewed_count+=1
                        elif(behaviortype.startswith("apply_meeting")):
                            _project_profile.apply_meeting_count+=1
                        elif(behaviortype=="replied"):
                            _project_profile.replied_count+=1
                        elif(behaviortype=="recommended"):
                            _project_profile.recommend_count +=1
                        elif(behaviortype=="marked"):
                            _project_profile.marked_count+=1
                        elif(behaviortype=="exposed" or behaviortype.startswith("project_expose") ):
                            _project_profile.exposed_count+=1
                        elif(behaviortype=="like"):
                            _project_profile.like_count +=1
                            #raw_input()

                        inc_viewed=0
                        inc_exposed=0

                        if(behaviortype=="viewed" or behaviortype.startswith("project_view") ):
                            inc_viewed=1
                        elif(behaviortype=="exposed" or behaviortype.startswith("project_expose") ):
                            inc_exposed=1

                        if(current_mode==_REALTIME):
                            update_project_stat_info(projectid,_project_profile)

                            if(projectid>0 and userid>0 and (inc_viewed > 0 or inc_exposed>0)):
                                #if not in realtime mode,just update in memory,only update db in realtime mode; and when the status changed (from history to realtime mode)
                                DataAccess.add_user_track_record (projectid,userid,inc_viewed,inc_exposed,_DEBUG)

                        elif(current_mode==_HISTORY):
                            if(projectid>0 and userid>0 and (inc_viewed > 0 or inc_exposed>0)):
                                if(total_user_track_count<50*10000):
                                    #update userid dict (value is another dict (key is project,value is exposed/view))
                                    _project_dict_exposed_view=None
                                    if(user_project_exposed_view.has_key(userid)):
                                        _project_dict_exposed_view=user_project_exposed_view[userid]
                                    else:
                                        _project_dict_exposed_view={}
                                        user_project_exposed_view[userid]=_project_dict_exposed_view

                                    _exposed_view_stat=[0,0]
                                    if(_project_dict_exposed_view.has_key(projectid)):
                                        _exposed_view_stat=_project_dict_exposed_view[projectid]
                                        #print 'need existed ',_exposed_view_stat
                                    else:
                                        _project_dict_exposed_view[projectid]=_exposed_view_stat

                                    _exposed_view_stat[0]+=inc_exposed
                                    _exposed_view_stat[1]+=inc_viewed
                                else:
                                    DataAccess.add_user_track_record(projectid,userid,inc_viewed,inc_exposed,_DEBUG)

                                #if(_exposed_view_stat[1]>2 or inc_viewed>1):
                                #    print 'need2rm _exposed_view_stat[1]',_exposed_view_stat[1],inc_viewed

                        bweight=behavior_weight[behaviortype]
                        if(bweight<=0):
                            continue

                        #ctr=float(_project_profile.viewcount)/ (1.0 + _project_profile.exposed_count)

    #                    if((current_timeStamp+3600*24*20)>timestamp_now  and current_mode!=_WEEKLY and behaviortype!="recommended" and behaviortype != "exposed"):
    #                        #update user track list (except weekly mode)
    #                        existed=0
    #                        u_p_k=str(userid)+"_"+str(projectid)
    #                        if(not u_p_dict.has_key(u_p_k)):
    #                            u_p_dict[u_p_k]=1
    #                        else:
    #                            existed=1
    #
    #                        redis_mng_user_track(userid,projectid)

    #                        if( not existed):
    #                            r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    #                            #need-update-
    #                            k=str(userid)
    #                            #k=str(userid)+'_track_new'
    #                            utracks=r.lrange(k, 0, -1)
    #                            if(utracks and len(utracks)>0):
    #                                rlen=r.llen(k)
    #                                for pii in utracks:
    #                                    pi=long(pii)
    #                                    #print '_____',pi,type(pi) ,projectid,type(projectid)
    #                                    if(pi == projectid):
    #                                        existed=1
    #
    #                                while(rlen>=MAX_UTRACK_LEN):
    #                                    r.lpop(k)
    #                                    rlen-=1
    #
    #                        if(not existed):
    #                            r.rpush(k, projectid)

                        #r1=r.lrange(k, 0, -1)
                        #sql = " SELECT eventid,userid,projectid,type,creationtime,fromstatus,tostatus,createby  FROM `mydb`.`project_investor_event` where eventid > "+str(eventid)+" ORDER BY `eventId` LIMIT 50;"
                        #weekday=createtime.weekday()
                        #print createtime,'weekday',weekday 

                        #timeArray = time.strptime(str(createtime) , "%Y-%m-%d %H:%M:%S")        
                        #print 'timeArray --' , timeArray 
                        #dateArray = time.strptime(str(createtime) , "%Y-%m-%d %H:%M:%S")        
                        #current_timeStamp = int(time.mktime(timeArray))    

                        #for realtime mode,just process data one by one
                        if(current_mode==_REALTIME):
                            if(behaviortype=="filter_label__##"):
                                print 'should hot run this part and be error',_eventid
                                if(len(filterinterest_for_new)>1):
                                    interest_selected_list=filterinterest_for_new.split(',')
                                    for interest_front1 in interest_selected_list:
                                        interest_front=interest_front1.strip()
                                        if(len(interest_front)<2):
                                            continue
                                        if(not front_back_mapping.has_key(interest_front)):
                                            continue
                                        back_keys_dict=front_back_mapping[interest_front]
                                        for keyword in back_keys_dict.keys():
                                            p_type_time=[0,behaviortype,current_timeStamp,keyword ]
                                            user_tract_dict[userid].append(p_type_time)

                            else:
                                p_type_time=[projectid,behaviortype,current_timeStamp]
                                user_tract_dict[userid].append(p_type_time)

                            weekly_data_porcess(begin_of_week_timestamp,user_tract_dict,_project_profile_dict,current_mode)
                            #after process each data
                            #print "re-create dict"
                            #after the weekly data process, the user_track_dict should be vanished
                            user_tract_dict=defaultdict(list)
                            if(switch_interest_new==0):
                                writefile4int(last_projectid_file,eventid)
                            elif(switch_interest_new==1):
                                writefile4int(last_projectid_file_for_label,eventid_filter_label)
                            else:
                                writefile4int(last_projectid_file_new_interest,eventid_new_interest)

                            continue

                        #for the first time or too many data to process or cross the week
                        if(begin_of_week_timestamp==0 or current_timeStamp > end_of_thisweek_timestamp or (current_timeStamp<1425073577 and addcount>1000)): # or (addcount>10000 and current_mode==1 )):
                            userprofilelogger.info('---begin_of_week_timestamp-'+str(begin_of_week_timestamp)+'--current_timeStamp--'+str(current_timeStamp)+'--end_of_thisweek_timestamp-'+str(end_of_thisweek_timestamp)+'--addcount-'+str(addcount))
                            #cross the week or too old or too many data to process
                            if((begin_of_week_timestamp!=0 and current_timeStamp > end_of_thisweek_timestamp) or (current_timeStamp<1425073577 and addcount>1000)):# or (addcount>10000) ):
                                #print "process this week 's data",addcount ,'begin_of_week_timestamp',begin_of_week_timestamp,'end_of_thisweek_timestamp',end_of_thisweek_timestamp
                                weekly_data_porcess(begin_of_week_timestamp,user_tract_dict,_project_profile_dict,current_mode)
                                #raw_input()
                                #print "re-create dict"
                                #after the weekly data process, the user_track_dict should be vanished
                                user_tract_dict=defaultdict(list)
                                addcount =0

                            weektime_is_zero=0
                            if(begin_of_week_timestamp==0):
                                weektime_is_zero=1

                            begin_of_week_timestamp=current_timeStamp 
                            date_time_=time.localtime(begin_of_week_timestamp)
                            tmy=date_time_.tm_year
                            tmm=date_time_.tm_mon
                            tmd=date_time_.tm_mday

                            tmw=date_time_.tm_wday
                            zero_of_thisday=datetime.datetime(tmy,tmm,tmd)

                            #print 'zero_of_thisday', zero_of_thisday
                            #timeArray_end = time.strptime(str(zero_of_thisday) , "%Y-%m-%d %H:%M:%S")        
                            #zero_timeStamp = int(time.mktime(timeArray_end ))    

                            dtt_end = zero_of_thisday.timetuple() 
                            zero_timeStamp = time.mktime(dtt_end ) # 1293868800.0

                            end_of_thisweek_timestamp= zero_timeStamp + (7-tmw)*24*3600 #-1
                            #end_date_time_=time.localtime(end_of_thisweek_timestamp)

                            if(current_mode!=_REALTIME):
                                #should also update user's weekly profile
                                if(current_mode==_WEEKLY or (current_mode==_HISTORY and (current_timeStamp > (end_of_thisweek_timestamp_lastweek-3600*12)) and current_timeStamp < end_of_thisweek_timestamp_lastweek)):
                                    #for weekly just record both
                                    writefile4int(last_maxid_in_lastweek,eventid)
                                    writefile4int(last_maxid_in_lastweek_new_interest,eventid_new_interest)
                                    writefile4int(last_maxid_in_lastweek_for_label,eventid_filter_label)
                                    #userprofilelogger.info('-update weekly--begin_of_week_timestamp-'+str(begin_of_week_timestamp)+'-eventid--'+str(eventid)+'--eventid_new_interest--'+str(eventid_new_interest)+'--eventid_filter_label-'+str(eventid_filter_label))

                                    #finish the weekly update,just switch baock to realtime/history mode
                                    if(weektime_is_zero==0 and current_mode==_WEEKLY and current_timeStamp > begin_of_thisweek_timestamp_now  ):
                                        userprofilelogger.info('--end of weekly')
                                        return _WEEKLY

                                    #exit()
                                #set last week's max eventid from redis/mysql
                                pass
                            #update last eventid
                            if(current_mode!=_WEEKLY):
                                if(switch_interest_new==0):
                                    writefile4int(last_projectid_file,eventid)
                                elif(switch_interest_new==1):
                                    writefile4int(last_projectid_file_for_label,eventid_filter_label)
                                else:
                                    writefile4int(last_projectid_file_new_interest,eventid_new_interest)


    #                    p_type_time=[projectid,behaviortype,current_timeStamp]
    #                    print '---projectid--', projectid,behaviortype,current_timeStamp
    #                    if(projectid<0):
    #                        print '-error--projectid--', projectid,behaviortype,current_timeStamp
    #                        raw_input()

                        #user_tract_dict[userid].append(p_type_time)

                        if(behaviortype=="filter_label__##"):
                            print 'should be error',_eventid
                            if(len(filterinterest_for_new)>1):
                                interest_selected_list=filterinterest_for_new.split(',')
                                for interest_front1 in interest_selected_list:
                                    interest_front=interest_front1.strip()
                                    if(len(interest_front)<2):
                                        continue
                                    if(not front_back_mapping.has_key(interest_front)):
                                        continue
                                    back_keys_dict=front_back_mapping[interest_front]
                                    for keyword in back_keys_dict.keys():
                                        p_type_time=[0,behaviortype,current_timeStamp,keyword ]
                                        user_tract_dict[userid].append(p_type_time)

                                        #print "behaviortype==filter_label__##",current_timeStamp
                                        #print 'press any key'
                                        #raw_input()

                        else:
                            p_type_time=[projectid,behaviortype,current_timeStamp]
                            user_tract_dict[userid].append(p_type_time)
                        addcount +=1

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
        if(sys.argv[1]=='_debug' or sys.argv[1]=='debug'):
            _DEBUG='_debug'
            update_redis_debug(_DEBUG)
    else:
        trytimes=0
        while(trytimes<3):
            print 'start with online version'
            sleep(5)
            trytimes+=1
        print 'really not input the _debug parameter?'
        sleep(15)


    userprofilelogger_name = 'log_userprofile'+_DEBUG
    print userprofilelogger_name 
    userprofilelogger = Logger.initlog(userprofilelogger_name)

    print 'begin check file',first_round_file
    userprofilelogger.info('first check file '+first_round_file)
    trytimes=0
    while(trytimes<3):
        if not os.path.exists(first_round_file):
            userprofilelogger.info('should we create the file for first round touch '+first_round_file)
            print 'should we create the file for first round',first_round_file
            print 'if first ,should use : touch ',first_round_file
            sleep(10)
            trytimes+=1
        else:
            break

    get_mapping_back_front_cate()
    get_user_with_new_interest_dict()

    #process("")#dir_path + filename)

    #get_project_profile()

    #ident1=thread.start_new_thread(get_project_profile_increment,())  
    get_project_profile_increment()

    for_new_changed_data=1
    #get_project_profile(for_new_changed_data)
    thread.start_new_thread(get_project_profile_newly_changed,())  

    thread.start_new_thread(get_project_profile_front,())  

    sleep(3)

#    while(1):
#        sleep(3)
#    exit()

    #we treat the whole data as different time-period (total history,except this week's;  realtime (in this week,update profile with weight*1.2),weekly (when in realtime mode, change back to weekly, based on last week's profile,and process from the last processed data in last week; (old*0.8 + data_in_this_week),then, switch back to realtime mode)

    while(1):
        #print '----------------------- buzcontrl 11',time.strftime("%Y-%m-%d %H:%M:%S")        
        userprofilelogger.info('----------------------- buzcontrl 11--'+str(time.strftime("%Y-%m-%d %H:%M:%S")))
        ret=business_contrl()
        #currently it's in realtime mode,switch to weekly mode
        userprofilelogger.info('-----------------------buzcontrl 000 inner--'+str(time.strftime("%Y-%m-%d %H:%M:%S"))+"--"+str(ret))
        if(ret==_REALTIME):
            userprofilelogger.info('---weekly--------------------buzcontrl 22 '+str(time.strftime("%Y-%m-%d %H:%M:%S")))
            ret=business_contrl(_WEEKLY)

    #for filename in files:
    #    topic_list = []
    #if re.match(re.compile(r'^result_url'),filename):


    print 'over--'
