#usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
from DataAccess import *
from DataAccess_IR import *
#from dedup_cluster import *
from getall_sentences import *
from stockseg import *
from category_sim import *
import Logger
import traceback
import UbClient
import mcpack
import time
from time import sleep

import socket
import struct
import json
import math
from collections import defaultdict
from strip_prefix import *
from team_classify import *

from constant import *
from data_dao import *
from pdb import *
#import redis

obj_topic_id = re.compile(r'^topic_id')
obj_best_title = re.compile(r'^best_title:')
obj_page_id = re.compile(r'^id:')
obj_delimi = re.compile(r'\t')
topic_list = []
#logger = Logger.initlog('write_url11.log')

dbhost = "irweb"
#dbport = 2026 
dbport = 2016 

BOOsT_4_BOTH_TAG_TERM=0.2
DEMOTE_4_DELIMETER=0.001
#MAX_OCCURANCE=2**16-1
MAX_OCCURANCE=255
CATEGORY_BEGIN=200
CONTENT_BEGIN=500
DELIMETER=chr(3)

#CONTENT_SPLIT="cntntsplt "
TITLE_SPLIT="ttlsplit "
TITLE_SPLIT_FILTER="ttlsplit"

CONTENT_SPLIT="cntntsplt "
CONTENT_SPLIT_FILTER="cntntsplt"

ONLINE_PROJECT=1
OFFLINE_PROJECT=2
FUND=4  #with id < 0
LEADS=8 #with id < -3000*10000
INVESTOR=16 #with id < -1000*10000
NEWS=32
INVESTMENT=64 #with id < -6000*10000
NEWS_INVESTMENT=128 #with id < -9000*10000
CRAWLED_LEADS_NOT_SYNCED=256 #with id < (-1)*(12000*10000+pid)

_PRJ_WITH_AGENT=1
_PRJ_OFFLINE=2
_PRJ_ONLINE=4

result_delimeter=chr(3)
dilimeter_dict={}
dilimeter_list=[]
logger = Logger.initlog('log_project_transfer.log')

illegal_sents=["【简介】", "【一句话】", "【官网】", "【报道】", "【融资情况】", "【来源】", "【项目介绍】", "【网站】", "【坐标】", "【阶段】", "【成立时间】", "【电话】", "【邮箱】","【创立时间】","【城市】"]

def delimiter_init():
    global dilimeter_dict
    global dilimeter_list
    #dilimters = "~!@#$%^&*()_+~！@#￥%……&*（）——+{}“：？》《}{\":?><[];'/.,】【‘；、。，·-=·-=\|"
    dilimters = "()_￥……（）——+{}“：？》《}{\":?><[]】【‘；、。，·-=·.-=\|"
    dilimters = dilimters.decode("utf-8")
    dilimter_array = list(dilimters)

    dindex=1
    for d1 in dilimter_array:
        #print d1,dindex
        d=d1
        try:
            d=d.encode("utf-8")
        except:
            print 'encode error for deimeter',d

        if(not dilimeter_dict.has_key(d)):
            dilimeter_dict[d]=1
            dilimeter_list.append(d)
        dindex+=1

    #print "in dict\n"

    #dindex=1
    #for d in dilimeter_dict.keys():
        #print d,dindex
    #    dindex+=1



def get_team_founder_feature(team_feature_dict):

    team_feature_term=""
    if(team_feature_dict!=None):
        for k,v in team_feature_dict.iteritems():
            team_feature_term+="F_"+str(k)+"\t0.001\t1\t1\t"

    return team_feature_term.strip().strip('\t')

def sequence_encode(terms):
    termarr=terms.split('\t')
    encodestr=""
    for a in termarr:
        arr=a.split(DELIMETER)
        index=0
        if(len(arr)>0):
            b = arr[0]
            try:
                b= b.decode("gbk").encode('utf-8','ignore')  
                encodestr+=a+"\t"
            except:
                pass
                #print 'sequence encode error'

    encodestr=encodestr.strip('\t')
    try:
        encodestr= encodestr.decode("gbk").encode('utf-8','ignore')  
    except:
        print 'total sequence encode error'
    #print 'encodestr:',encodestr
    return encodestr


def getparser(title,content,con,logger,dedup):
    pok=0
    termstr=""
    tryTimes=0;
    __termCountInTitlte=0
    __terms=""
    __termCount=0

    while(tryTimes < 3):
        tryTimes=tryTimes+1
        #try:
        if(1):
            if(con==None):
                dbtype = "socket"
                dbfile = ""
                dbwto =2000
                dbrto =2000
                #logger = Logger.initlog("./con_sock_log")

                #print 'debug dbport',  dbport 
                con = UbClient.Connector(dbtype, dbhost, dbport, dbfile ,dbwto, dbrto, logger) 
                con.sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack('ii', 1, 0))
        
            reqdata = {}
    
            reqdata["title"]=title  
            reqdata["content"]=content
            reqdata["aid"]=0
            reqdata["pubtime"]=0
            reqdata["is_dedup"]=dedup

            req_pack = mcpack.dumps_version(mcpack.mcpackv1, reqdata, 4*1024*1024)
            con.write_pack(req_pack)
            (ret ,res_pack) = con.read_pack()
            pok=1
            if ret == 0:
                resdict = mcpack.loads(res_pack)
                
                __terms=resdict["terms"] #.replace("'"," ") 
                try:
                    __terms = __terms.decode("gbk").encode('utf-8','ignore')  
                except:
                    #print 'decode or encode error:',"title:["+title+"]",__terms,content
                    #print __terms,content
                    __terms=sequence_encode(__terms)

                __termCount=resdict["termCount"]

                __termCountInTitlte=resdict["termCountInTitlte"]

                #print title
                #print __terms

                break;
    
        #except:
        if(0):
            print 'except-sock-',sys.exc_info()[0]
            con.sock.close()
            sleep(1)#con.sock.close()
            con=None

#'''    
#        if(con!=None):
#            con.sock.close()
#            con=None
#'''

    return __termCount,__terms,con,__termCountInTitlte





def get_project_attribute(projectid,categoryid):

    catestr=""
    attributestr=""
    qstr=""
    kdstr=""

    allcategories=""

    #categoryid = 0
    _category_dict={}
    attribute_processed_dict={}
    attribute_dict={}

    totalweight=0.0
    a_list=[]

    #get real category
    
    if(1):
        results = DataAccess.get_project_attributes(projectid)

        #print 'result len list',len(results)
        categoryindex=1

        if(results and len(results)>0):

            if(categoryid>0):
                cate_processed=1
                p_s_k=get_parent_subcate(categoryid)
                if(p_s_k!=""):
                    if(not _category_dict.has_key(p_s_k)):
                        _category_dict[p_s_k]=1
                else:
                     print 'category is empty',projectid

            cate_processed=0

            for r in results:
                #sql = "SELECT projectid,attributeid,value,id FROM `mydb`.`project_category_backend` where projectid= "+str(projectid)+" ORDER BY `id` "
                projectid= r[0]
                attributeid = r[1]

                value = r[2]
                if(value ==None or value==""):
                    continue
                    
                value = value.encode("utf-8")

                value = value.strip("\t").strip().strip("\t")
                if(len(value)==0):
                    continue

                #categoryid=get_cid_by_aid(attributeid)
                    #kdstr+=p_s_k+"\t"
                    #print 'parent_sub_k',p_s_k

                value = value.lower()

                arr=value.split(",")


                weight=getattributeweight(attributeid)

                for v1 in arr:
                    v=v1.strip()
                    if(len(v)==0):
                        continue
                    if(getfiltered(v)):
                        #print 'filtered',v
                        continue
                        
                    if(attribute_processed_dict.has_key(v)):
                        #print 'attribute-------already exit'
                        continue

                    attribute_processed_dict[v]=1

                    weight=getattributeweight(attributeid)

                    othercategoryid=get_cid_by_aid(attributeid)
                    #print 'othercategoryid', othercategoryid,'attributeid',attributeid
                    #raw_input()
                    if(othercategoryid!=categoryid):
                        #treat as subsidiary category,instead of attribute
                        if(weight>100.0):
                            #print 'got a category,category is ',v,'weight',weight
                            #catestr+="T1="+p_s_k+"\tTw1=1\t"
                            _subsidiary_s_k="T_"+v
                            #print 'subsidiary',_subsidiary_s_k

                            if(not _category_dict.has_key(_subsidiary_s_k)):
                                #print 'not has this subsidiary',_subsidiary_s_k
                                _subsidiary_weight=0.4

                                _category_dict[_subsidiary_s_k]=_subsidiary_weight

                            continue

                    a_existed=0
                    if(attribute_dict.has_key(v)):
                        a_existed=1

                        old_weight=attribute_dict[v]
                        if(old_weight<weight):
                            attribute_dict[v]=weight
                            totalweight += weight * weight-old_weight*old_weight


                    else:
                        attribute_dict[v]=weight
                        totalweight += weight * weight

                    if(a_existed==0):
                        a_w=[v,weight]
                        a_list.append(a_w)




    total_cate_weight=0.0
    for c,w in _category_dict.items():
        total_cate_weight += w*w
                            
    total_cate_weight =math.sqrt(total_cate_weight )

    if(total_cate_weight<0.001):
        total_cate_weight+=0.001

    categoryindex=1
    sortedcates= sorted(_category_dict.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
    for c_w in sortedcates: #_category_dict.items():
        c=c_w[0]
        w=c_w[1]
        currentweight=w #0.0

        currentweight/=total_cate_weight 

        #if(total_cate_weight>0.01):
        #    currentweight=w/total_cate_weight

        #total_cate_weight+=0.001
        catestr+="T"+str(categoryindex)+"="+c+"\tTw"+str(categoryindex)+"="+str(currentweight)+"\t"

        allcategories += c+"\t"

        #print 'all catestr',catestr
        qstr+=c+"\t"+str(currentweight)+"\t"
        categoryindex+=1


    #print 'categoryid',categoryid,'catestr:',len(catestr),catestr
    #raw_input()

    #to process the attribute & its weight
    aindex=0
    totalweight=math.sqrt(totalweight)

    for a_w in a_list:
        v=a_w[0]
        weight=attribute_dict[v]
        #weight=a_w[1]

        aindex+=1
        singleweight=0.0
        if(totalweight>0.0):
            singleweight=weight/totalweight

        k4value="K_"+v
        attributestr+="K"+str(aindex)+"="+k4value+"\t"+"KW"+str(aindex)+"="+str(singleweight)+"\t"
        qstr+=k4value+"\t"+str(singleweight)+"\t"

        #kdstr+=k4value+"\t"
                    #print aindex,'pid',projectid,k4value,weight #'aid',attributeid,v,'weight',weight
                        
                    
    allcategories = allcategories.strip()
    return catestr,attributestr,qstr,kdstr,categoryid,allcategories 



def get_project_expire(projectid,expiretime):

    expired=0
    results = DataAccess.get_project_expire(projectid)

    if results==None or len(results)==0:
        expired=1

    if results:
        for result in results:
            creationtime = str(result[0])

            #print creationtime ,'expired',  expiretime,'projectid',projectid

            if(creationtime <  expiretime):
                expired=1
    
            break

    return expired


def format_field(field,totalstr):
    if(field == None):
        return totalstr
        
    field = field.strip()
    if(len(field)==0):
        return totalstr
        
    field = field.encode('utf-8','ignore')
    #totalstr += field + " "
    totalstr += field + chr(4)
    return totalstr 


def get_project_comments(projectid):
    comments=""
    results = DataAccess_IR.get_project_comments_(projectid)

    if results:
        for result in results:
            try:
                #sql = " SELECT name,`weixin`,`email` ,`phone`,`info` FROM `mydb`.`project_team_info`
                _c = result[0]
                if(_c == None):
                    continue

                _c = _c.strip()
                _c = _c.encode('utf-8','ignore')
                    
                comments +=  _c+" "

            except:
                print "traceback", traceback.print_exc() ,projectid

    comments=comments.strip()
    comments=comments.lower()

    sentlist=getallsents(comments)
    realcontent = ""
    sent_dict={}
    for sent in sentlist:
        if(sent_dict.has_key(sent)):
            continue
        sent_dict[sent]=1

        realcontent +=sent+chr(4)
    content=realcontent 
    return content


def get_teaminfo_byeditor(projectid,forapp=None):

    teaminfoall=""
    results = DataAccess_IR.get_team_all_info_by_editor(projectid)

    if results:
        for result in results:
            try:
                #sql = " SELECT name,`weixin`,`email` ,`phone`,`info` FROM `mydb`.`project_team_info`
                uname = result[0]
                if(uname == None):
                    continue

                uname = uname.strip()
                uname = uname.encode('utf-8','ignore')
                    
                teaminfoall += uname+" "

                if(forapp!=None):
                    weixin= result[1]
                    teaminfoall = format_field(weixin,teaminfoall)

                    email= result[2]
                    teaminfoall = format_field(email,teaminfoall)

                    phone= result[3]
                    teaminfoall = format_field(phone,teaminfoall)

                info = result[4]
                teaminfoall = format_field(info,teaminfoall)

            except:
                print "traceback", traceback.print_exc() ,pid

    teaminfoall=teaminfoall.strip()
    teaminfoall=teaminfoall.lower()
    return teaminfoall

def html_encode(s):

    htmlCodes = (
            ('>', '&gt;'),
            ('<', '&lt;'),
            )
    for code in htmlCodes:
        s = s.replace(code[0], code[1])
        #print code[1], code[0],s
        
    return s



def term_extract(title,content,con,logger,dedup,cate_dict):
    global dilimeter_dict
        
    termstr=""
    tag_dict={}
    total_arr=[]

    term_list=[]

    if(1):
        titlearr=[]
        contentarr=[]


        termcount,terms,con,__termCountInTitlte=getparser(title,content,con,logger,dedup )
        #print 'debug afte r seg',title,'terms]]]',terms,'chr777',terms.replace(chr(7),"'"),con,__termCountInTitlte
        #print 'content to parser debug ',content
        termcount=int(termcount)
        __termCountInTitlte=int(__termCountInTitlte)
        #print 'debug',title,content
        #print "debug aaaaaaaaaaa",__termCountInTitlte,termcount,terms
        #print 'need2rm'
        #print termcount,terms
        #print termcount,terms,con,title,content,con,logger,dedup 
        #os._exit(1)

        terms=terms.strip()

        total_termweight=0;
        realtindex=0
        tindex=0

        terms=terms.strip("\t").strip()
        #print title,'terms"""',terms
        if(len(terms)>1):
            termarr=terms.split("\t")
            term_processed={}

            #try:
            if(1):
                term_weight_dict=defaultdict(float)

                termcount_in_realtitle=0;
                termcount_in_content=0;
                termcount_in_realtitle_dedup=0;
                found_title_end=0
                found_content_end=0

                while(tindex<len(termarr)):
                    #print ' termarr[tindex]',termarr[tindex],len(termarr),tindex,terms[:128]
                    tarr=termarr[tindex].split(result_delimeter)
                    k=tarr[0]

                    #print 'k',k,tarr[1]

                    #print 'k',tindex,k

                    if(found_title_end==0 and tindex < __termCountInTitlte):

                        if(k==TITLE_SPLIT_FILTER):
                            termcount_in_realtitle=tindex;
                            found_title_end=1
                            tindex+=1
                            continue

                        if(not term_weight_dict.has_key(k)):
                            termcount_in_realtitle_dedup+=1


                    if(tindex >= __termCountInTitlte):

                        if(k==CONTENT_SPLIT_FILTER):
                            found_content_end=1

                        if(found_content_end==0):
                            termcount_in_content+=1

                        #termcount_in_content+=1

                    if(found_title_end==0):
                        titlearr.append(k);
                    

                    if(tindex >= __termCountInTitlte):
                        contentarr.append(k)

                    if(k!=CONTENT_SPLIT_FILTER and k!=TITLE_SPLIT_FILTER):
			if(not (k>=chr(2) and k<=chr(8))):
			    term_list.append(k)


                    #print 'k:['+k+']tarr[1]', tarr[1],tindex,len(termarr)#,termarr[0:33]
                    termweight=int(tarr[1])

                    if(dilimeter_dict.has_key(k)):
                        termweight*=DEMOTE_4_DELIMETER
                        termarr[tindex]=k+result_delimeter+str(termweight)

                    term_weight_dict[k]+=termweight
                    tindex+=1


                #print __termCountInTitlte,"termcount_in_realtitle:",termcount_in_realtitle
                #os._exit(1)

                tindex=0
                real_term_index=0
                is_content_begin=0

                while(tindex<len(termarr)):
                    #print 'second round'
                    #raw_input()
                    tarr=termarr[tindex].split(result_delimeter)
                    k=tarr[0]
                    if(k==chr(6) or k==chr(4)):
                        tindex+=1
                        continue

                    #if(k!=chr(4)):
                        
                    real_term_index+=1

                    nomalized_tindex = real_term_index

                    #print 'debug:',"tindex >=  __termCountInTitlte",tindex,"__termCountInTitlte:",__termCountInTitlte ,tindex >=  __termCountInTitlte
                    if(tindex >=  __termCountInTitlte):
                        #just make offset/sequence of the term in content bigger than 50
                        if(is_content_begin==0):
                            is_content_begin=1
                            real_term_index=0

                        nomalized_tindex = CONTENT_BEGIN + real_term_index
                    elif(tindex >  termcount_in_realtitle):
                        #print 'in else::::debug:',"tindex >=  __termCountInTitlte",tindex,"__termCountInTitlte:",__termCountInTitlte ,tindex >=  __termCountInTitlte
                        nomalized_tindex = CATEGORY_BEGIN + real_term_index

                    #print 'debug:',k,nomalized_tindex ,tindex,"__termCountInTitlte",__termCountInTitlte,"termcount_in_realtitle",termcount_in_realtitle

                    if(term_processed.has_key(k)):
                        #term_processed[k].append(tindex)
                        term_processed[k].append(nomalized_tindex )
                        tindex+=1
                        continue

                    term_processed[k]=[nomalized_tindex ]

                    termweight=term_weight_dict[k]
                    total_termweight+=termweight*termweight
                    #print 'termweight___k',termweight,k,'total_termweight',total_termweight
                    tindex+=1
            #except:
            #    print 'except',tindex,len(termarr),termarr,len(terms)

            f_total_termweight=float(total_termweight);

            #print 'f_total_termweight=float(total_termweight);',f_total_termweight

            f_total_termweight=math.sqrt(f_total_termweight)

            tindex=0
            keywordstr_=""

            term_forward_processed={}

            while(tindex<len(termarr)):
                tarr=termarr[tindex].split(result_delimeter)
                k=tarr[0]

                if(k==chr(6) or k==chr(4)):
                    tindex+=1
                    continue

                if(term_forward_processed.has_key(k)):
                    tindex+=1
                    continue
                term_forward_processed[k]=1

                #print tarr,len(tarr),tindex,len(termarr)
                #termweight=float(tarr[1])
                termweight=term_weight_dict[k]

                if(cate_dict.has_key(tarr[0])):
                    #termweight+=highestweight
                    termweight+=BOOsT_4_BOTH_TAG_TERM
                    #print 'term weight boost',termweight

                if(f_total_termweight<0.001):
                    termweight=0.0
                else:
                    termweight /=f_total_termweight
                    
                #print 'kkkkk', k
                occurance_list = term_processed[k]
                occurance_count = len(occurance_list)
                if(occurance_count > MAX_OCCURANCE):
                    occurance_count = MAX_OCCURANCE

                #occur_arr=[]
                #oi=0
                #for o in occurance_list:
                #    #occurlist+=str(o)+"\t"
                #    occur_arr.append(str(o))
                #    occur_arr.append("\t")
                #    oi+=1
                #    if(oi>=occurance_count):
                #        break
                #    
                #occurlist="".join(occur_arr)
                #occurlist=occurlist.strip("\t")

                #single_term_forward_index=tarr[0] +"\t" + str(termweight) +"\t"+str(occurance_count)+"\t"+occurlist+"\t"
                #term \t term_weight \t occurance_count \t occurlist
                #termstr+=single_term_forward_index 

                termweight=float('%0.5f' % termweight)

                if(k and len(k)>0):
                    tag_dict[k]=termweight
		#    k_with_occur=[k,occurance_count]
		#    k_with_occur+=occurance_list
                #    total_arr.append(k_with_occur)
                    #total_arr.append(k)
                    #total_arr.append("\t")
                    #total_arr.append(str(termweight))
                    #total_arr.append("\t")
                    #total_arr.append(str(occurance_count))
                    #total_arr.append("\t")
                    #total_arr.append(str(occurlist))
                    #total_arr.append("\t")

                tindex+=1

            #termstr="".join(total_arr)

    #tag_with_occur=total_arr
    return tag_dict,term_list	#tag_with_occur
    
def replace_dilimeter(sent):
    global dilimeter_list
    for d in dilimeter_list:
        sent=sent.replace(d,chr(5))
        
    return sent

def verify_field(f):
    isempty=1
    if(f==None):
        return isempty,""
    f=f.encode('utf-8','ignore').strip()
    isempty=0

    return isempty,f

def normalize_field(f,content):
    if(f==None):
        return "",content
    f=f.encode('utf-8','ignore').strip()
    if(f!=""):
        if(content!=""):
            content+="|"
        content+=f

    return f,content



def get_fund_fav(fundid):
    total_fav=""
    if(1):
        results = None
        results = DataAccess_IR.get_fund_fav(fundid)

        if results==None or len(results)==0:
            return total_fav

        if results:
            try:
            #if(1):
                for result in results:
                    favestr = result[0]
                    if(favestr ==None):
                        continue
                    favestr = favestr.encode('utf-8','ignore')
                    favestr = favestr.strip()
                    if(favestr == ""):
                        continue

                    if(total_fav!=""):
                        total_fav+=favestr +"|"
                    else:
                        total_fav=favestr +"|"
            except:
                print 'get user fav error',userid

    total_fav=total_fav.strip("|").strip()
    return total_fav

def get_user_subed(userid):
    total_fav=""
    if(1):
        results = None
        results = DataAccess_IR.get_investor_subed(userid)

        if results==None or len(results)==0:
            return total_fav

        if results:
            try:
            #if(1):
                for result in results:
                    favestr = result[0]
                    if(favestr ==None):
                        continue
                    favestr = favestr.encode('utf-8','ignore')
                    favestr = favestr.strip()
                    if(favestr == ""):
                        continue

                    favestr = favestr.lower()
                    if(total_fav!=""):
                        total_fav+=favestr +"|"
                    else:
                        total_fav=favestr +"|"
            except:
                print 'get user fav error',userid

    total_fav=total_fav.strip("|").strip()
    return total_fav

def get_user_industry_query(userid):
    total_fav=""
    if(1):
        results = None
        results = DataAccess_IR.get_investor_industry_query(userid)

        if results==None or len(results)==0:
            return total_fav

        if results:
            try:
            #if(1):
                for result in results:
                    favestr = result[0]
                    if(favestr ==None):
                        continue
                    favestr = favestr.encode('utf-8','ignore')
                    favestr = favestr.strip()
                    if(favestr == ""):
                        continue

                    favestr = favestr.lower()
                    if(total_fav!=""):
                        total_fav+=favestr +"|"
                    else:
                        total_fav=favestr +"|"
            except:
                print 'get user fav error',userid

    total_fav=total_fav.strip("|").strip()
    return total_fav


def get_user_fav(userid):
    total_fav=""
    if(1):
        results = None
        results = DataAccess_IR.get_user_fav(userid)

        if results==None or len(results)==0:
            return total_fav

        if results:
            try:
            #if(1):
                for result in results:
                    favestr = result[0]
                    if(favestr ==None):
                        continue
                    favestr = favestr.encode('utf-8','ignore')
                    favestr = favestr.strip()
                    if(favestr == ""):
                        continue

                    favestr = favestr.lower()
                    if(total_fav!=""):
                        total_fav+=favestr +"|"
                    else:
                        total_fav=favestr +"|"
            except:
                print 'get user fav error',userid

    total_fav=total_fav.strip("|").strip()
    return total_fav


def update_news():

    newsid =0

    total_news_count=0
    
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_news_list(newsid)

            if results==None or len(results)==0:
                print 'no result',newsid
                break

            print 'total_news_count-'+str(total_news_count)+'--get_new result len:',len(results),' newsid :',newsid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))

            if results:
                con=None
                try:
                    for result in results:
                        newsid = result[0]


                        dupids=result[4]
                        if(dupids==None):
                            dupids=""
                        else:
                            dupids=dupids.encode('utf-8','ignore')

                        pubtime =result[5]
                        if(pubtime == None):
                            pubtime =creationtime 
                        else:
                            pubtime =str(pubtime)

                        DataAccess_IR.update_news_ir(newsid,pubtime ,dupids)

                        #print 'debug---------'
                        #os._exit(-1)


                finally:
                    pass
    #except:
    #    print 'fund error',newsid

    print 'total_news_count', total_news_count



def get_news(rescan):

    newsid =0

    if(rescan==None):
        newsid = DataAccess_IR.get_last_newsid()
        newsid -=2000

    print 'last newsid ', newsid 

    creationtime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    updatetime = str(time.strftime("%Y-%m-%d %H:%M:%S"))

    total_news_count=0
    
    #try:
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_news_list(newsid)

            if results==None or len(results)==0:
                print 'no result',newsid
                break

            print 'total_news_count-'+str(total_news_count)+'--get_new result len:',len(results),' newsid :',newsid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))
            #sql = " select aid,url,title,content from doc_tab where aid > "+str(pid)+" order by aid limit 1;"

            if results:
                con=None
                try:
                    for result in results:
                        newsid = result[0]

                        title= result[1]
                        if(title==None or title==""):
                            continue

                        title=title.encode('utf-8','ignore')

                        dupids=result[4]
                        if(dupids==None):
                            dupids=""
                        else:
                            dupids=dupids.encode('utf-8','ignore')

                        isempty,content=verify_field(result[2])
                        isempty,url=verify_field(result[3])
                        
                        pubtime =result[5]
                        if(pubtime == None):
                            pubtime =creationtime 
                        else:
                            pubtime =str(pubtime)

                        sentlist=getallsents(content)
                        #sentindex=0
                        realcontent = ""
                        for sent in sentlist:
                            realcontent +=sent+chr(4)
                            if(len(realcontent)>128):
                                break
                        content=realcontent 

                        title = title.replace('\t',' ')
                        #title =title.replace("'"," ")

                        title_cate_field=title + " "+TITLE_SPLIT

                        title_cate_field=title_cate_field.lower()

                        content_with_team=content.replace("\t",' ')
                        content_with_team=content_with_team.lower()

                        title_cate_field=title_cate_field.replace( "'"," ")
                        content_with_team=content_with_team.replace( "'"," ")


                        title_cate_field = title_cate_field.replace(" ", chr(5))
                        content_with_team=content_with_team.replace(" ",chr(5))

                        title_cate_field = title_cate_field.replace("\r", chr(5)).replace("\n", chr(4))
                        content_with_team=content_with_team.replace("\r", chr(5)).replace("\n", chr(4))

                        dedup=16
                        

                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.strip("\t")
                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.replace("\\",'\\\\')
                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.replace("'","\\'")

                        title_cate_field=realtitle#.replace( "'","\\'")
                        content_with_team=realcontent.replace( "'","\\'")
                        title=title.replace( "'","\\'")

                        termcount_in_content = int(math.log(2.0+1.0/(2.0+abs(termcount_in_content-100.0)),2)*10000)
                        normalized_newsid=newsid 
                        querystr=""
                        keywordstr_=""
                        catestr=""
                        attributestr=""
                        fieldliststr=""
                        attach=""
                        termstr=""
                        status=-30000
                        projectlevel=NEWS

                        total_news_count+=1

                        DataAccess_IR.add_news_ir(normalized_newsid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,pubtime ,pubtime ,keywordstr_,status,projectlevel,forword_index_with_occurance_pos,title_cate_field,content_with_team,termcount_in_realtitle,termcount_in_content ,url,dupids)

                        #print 'debug---------'
                        #os._exit(-1)


                finally:
                    pass
    #except:
    #    print 'fund error',newsid

    print 'total_news_count', total_news_count





#@profile
def get_leads(rescan):

    leadsid =0
    if(rescan==None):
        leadsid = DataAccess_IR.get_last_leadsid()
        if(leadsid != 0):
            leadsid=(-1)*leadsid-30000000
            print 'leadsid begin', leadsid

    creationtime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    _updatetime = str(time.strftime("%Y-%m-%d %H:%M:%S"))

    total_leads_count=0

    leads_title_dict={}
    
    #try:
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_leads(leadsid)

            if results==None or len(results)==0:
                print 'no result',leadsid
                break

            print 'get_leads result len:',len(results),' leadsid :',leadsid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))
            #sql = " SELECT id,title,`abstract`,`founderName`,`founderPhone` ,`founderWeixin` ,`founderEmail`,`comment`   FROM `mydb`.`project_leads` where id > "+str(pid)+" ORDER BY `id` LIMIT 500;"

            if results:
                con=None
                try:
                    for result in results:
                        leadsid = result[0]

                        title= result[1]
                        if(title==None or title==""):
                            continue

                        title=title.encode('utf-8','ignore')
                        title=title.strip().strip('\t')
                        #print 'debug33['+title 
                        title =title.replace(" ",chr(6))
                        title =title.replace("'",chr(7))
                        #if(rescan==None):
                        #    pass

                        normalized_leadsid=(-1)*(3000*10000+leadsid)
                        if(leads_title_dict.has_key(title)):
                            #rm previous projectid in previous round
                            previous_pid=leads_title_dict[title]
                            leads_title_dict[title]=normalized_leadsid

                            #keep the new one with same title
                            DataAccess_IR.rm_project_for_diffrent_round(previous_pid,normalized_leadsid)
                            #print 'debug previous_pid',previous_pid,'leadsid:',leadsid,normalized_leadsid,
                            #raw_input()
                            #continue

                        leads_title_dict[title]=normalized_leadsid
                        #for k,v in leads_title_dict.iteritems():
                        #    print '------------',k,v
                        #print '2222',title,len(title),len(leads_title_dict.keys()),len(leads_title_dict)

                        content=""
                        founderinfo=""
                        team_feature_type=""
                        team_feature_value=""
                        team_feature_dict=None

                        abstract = result[2]
                        if(abstract !=None and abstract !=""):
                            abstract =abstract.encode('utf-8','ignore')
                            abstract,founderinfo = getfounder(abstract)

                            if(founderinfo != ""):
                                team_feature_type,team_feature_value,team_feature_dict=team_feature_extractor(founderinfo)

                            abstract= stripprefix(abstract)#,1)

                            for s in illegal_sents:
                                abstract =abstract.replace(s,chr(4))

                            sentlist=getallsents(abstract)
                            realcontent =chr(4).join(sentlist)
                            content+=realcontent 
    
                        foundername,content=normalize_field(result[3],content)
                        founderphone,content=normalize_field(result[4],content)
                        founderweixin,content=normalize_field(result[5],content)
                        founderemail,content=normalize_field(result[6],content)


                        comments = result[7]
                        if(comments !=None and comments !=""):
                            comments =comments.encode('utf-8','ignore')
                            comments = stripprefix(comments)

                            for s in illegal_sents:
                                comments =comments.replace(s,chr(4))

                            sentlist=getallsents(comments)
                            realcontent =chr(4).join(sentlist)
                            #print 'realcontent =chr(4).join(sentlist)',realcontent 
                            content+=chr(4)+realcontent 

                        label = result[8]
                        if(label !=None and label !=""):
                            label =label.encode('utf-8','ignore')
                            if(label !="0"):
                                #print label 
                                label =label.replace("·","|")
                                #print 'after ',label 
                                #raw_input()
                                #print 'label =============',label 
                                content+="|"+label 

                            #continue

                        #print 'any key111',content,'\n\n\n'

                        _data = result[9]

                        #print 'debug -data',_data,'\n\n'

                        if(_data !=None and _data !=""):
                            _data =_data.encode('utf-8','ignore')
                            datadict= json.loads(_data) 
    
                            #print 'after ',_data ,type(datadict),datadict,leadsid

                            try:
                                #print 'datadict["abstract"]',_data ,'dict:',datadict#, datadict["abstract"]
                                #if(datadict.has_key("abstract")):
                                datacontent=get_leads_data_parser(datadict).strip()
                                #print 'datacontent', datacontent,'\n\n\n'
                                content+=chr(4)+datacontent

                                #for k,v in datadict.iteritems():
                                #    if(k=="abstract"):
                                #        _abstract_in_json=v #datadict["abstract"]
                                #        #print'_abstract_in_json', _abstract_in_json
                                #        if(_abstract_in_json!=""):
                                #            _abstract_in_json=_abstract_in_json.encode("utf-8")
                                #            sentlist=getallsents(_abstract_in_json)
                                #            realcontent =chr(4).join(sentlist)

                                #            content+=chr(4)+realcontent 
                                #        #print 'realcontent ',realcontent 
                                ##raw_input()

                            except:
                                print 'json-data parse error',leadsid 
                                pass

                        #print 'any key',content
                        #os._exit(1)
                                
                        updateTime = result[11]
                        if(updateTime ==None):
                            updateTime = _updatetime 
                        else:
                            updateTime = str(updateTime).strip()
                            updateTime = updateTime.encode('utf-8','ignore')
                            
                        stutuscc = result[12]
                        if(stutuscc == None):
                            stutuscc =0

                        status = result[13]
                        if(status == None):
                            status =0

                        status_combined=(status +100 ) << 48 | (stutuscc +100 ) << 32


                        title = title.replace('\t',' ')
                        title =title.replace("'"," ")

                        title_cate_field=title + " "+TITLE_SPLIT

                        title_cate_field=title_cate_field.lower()


                        content = content.lower() + " " + CONTENT_SPLIT+founderinfo.lower() 

                        content_with_team=content.replace("\t",' ')

                        #print 'debug content_with_team', content_with_team
                        #raw_input()

                        title_cate_field=title_cate_field.replace( "'"," ")
                        content_with_team=content_with_team.replace( "'"," ")


                        title_cate_field = title_cate_field.replace(" ", chr(5))
                        content_with_team=content_with_team.replace(" ",chr(5))

                        title_cate_field = title_cate_field.replace("\r", chr(4)).replace("\n", chr(4))
                        content_with_team=content_with_team.replace("\r", chr(4)).replace("\n", chr(4))

                        dedup=16
                        

                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.strip("\t")
                        term_feature_term=get_team_founder_feature(team_feature_dict)
                        if(term_feature_term!=""):
                            forword_index_with_occurance_pos += "\t"+term_feature_term

                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.replace("\\",'\\\\')
                        #print forword_index_with_occurance_pos 
                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.replace("'","\\'")
                        #print 'ater------------',forword_index_with_occurance_pos 

                        title_cate_field=realtitle#.replace( "'","\\'")
                        content_with_team=realcontent.replace( "'","\\'")
                        title=title.replace( "'","\\'")

                        #print 'termcount_in_content',  termcount_in_content 
                        #termcount_in_content = int(math.log(2.0+1.0/(2.0+abs(termcount_in_content-100.0)),2)*10000)
                        #print 'debug---termcount_in_content',  termcount_in_content 
    
                        querystr=""
                        keywordstr_=""
                        catestr=""
                        attributestr=""
                        fieldliststr=""
                        attach=""
                        termstr=""
                        status=-30000
                        projectlevel=LEADS

                        total_leads_count+=1

                        DataAccess_IR.add_project_ir(normalized_leadsid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,updateTime ,updateTime ,keywordstr_,status,projectlevel,forword_index_with_occurance_pos,title_cate_field,content_with_team,termcount_in_realtitle,termcount_in_content,None,None,stutuscc,team_feature_type,team_feature_value,status_combined)

                        _projectid= result[10]
                        #print '###>>>>>########',normalized_leadsid,_projectid
                        if(_projectid!=None and _projectid !=0):
                            DataAccess_IR.rm_project_for_diffrent_round(normalized_leadsid,_projectid) #,"dedupwithproject")
                            #print '###########',normalized_leadsid,_projectid

                        #print 'debug---------'
                        #print '['+content_with_team+']'
                        #os._exit(-1)


                finally:
                    pass
                        
                    
            #print 'debug---------'
            #break
    #except:
    #    print 'fund error',leadsid

    print 'total_leads_count', total_leads_count


def get_news_investment(rescan):
    pid =0
    if(rescan==None):
    #if(0):
        pid = DataAccess_IR.get_last_news_investment_id()
        if(pid != 0):
            print pid 
            pid =(-1)*pid -90000000
            print 'pid begin', pid 
    ctime = str(time.strftime("%Y-%m-%d %H:%M:%S"))

    total_news_investment_count=0
    
    #try:
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_news_investment(pid)

            if results==None or len(results)==0:
                print 'no result',pid
                break

            print 'get_news_investment result len:',len(results),' pid :',pid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))
            #sql="SELECT id,`title` ,url,`pub_time`,dupe_ids  FROM `mydb`.`news_leads` where id > "+str(pid)+" ORDER BY `id` LIMIT 500;"

            if results:
                con=None
                try:
                    for result in results:
                        pid = result[0]

                        title= result[1]
                        if(title==None or title==""):
                            #username=""
                            continue

                        title=title.encode('utf-8','ignore')

                        title =title.replace(" ",chr(6))
                        title =title.replace("'",chr(7))

                        url = result[2]
                        if(url !=None ):
                            url =url.encode('utf-8','ignore')
                        else:
                            url = ""


                        creationtime = result[3]
                        if(creationtime ==None ):
                            creationtime = ctime 
                        else:
                            creationtime = str(creationtime).encode("utf-8")
                            
                        updatetime = creationtime 

                        dupids = result[4]
                        if(dupids != None ):
                           dupids = dupids.encode('utf-8','ignore')
                        else:
                           dupids = ""

                        title =title.replace(" ",chr(6))
                        title =title.replace("'",chr(7))
                        title=title.lower()
                        content_with_team=""

                        title = title.replace('\t',' ')
                        title =title.replace("'"," ")
                        title_cate_field=title+" "+TITLE_SPLIT
                        
                        title_cate_field = title_cate_field.replace(" ", chr(5))

                        title_cate_field = title_cate_field.replace("\r", chr(5)).replace("\n", chr(5))

                        dedup=16
                        

                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.strip("\t")
                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.replace("\\",'\\\\')
                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.replace("'","\\'")

                        title_cate_field=realtitle#.replace( "'","\\'")
                        title=title.replace( "'","\\'")

                        #termcount_in_content = int(math.log(2.0+1.0/(2.0+abs(termcount_in_content-100.0)),2)*10000)
    
                        normalized_pid=(-1)*(9000*10000+pid)
                        querystr=""
                        keywordstr_=""
                        catestr=""
                        attributestr=""
                        fieldliststr=""
                        attach=""
                        termstr=""
                        status=-50000
                        projectlevel=NEWS_INVESTMENT
                        total_news_investment_count+=1

                        DataAccess_IR.add_project_ir(normalized_pid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,creationtime,updatetime,keywordstr_,status,projectlevel,forword_index_with_occurance_pos,title_cate_field,content_with_team,termcount_in_realtitle,termcount_in_content,url,dupids)
    
                        #print 'termcount_in_realtitle' ,termcount_in_realtitle
                        #os._exit(1)


                finally:
                    pass
    #except:
    #    print 'fund error',pid

    print 'total_news_investment_count', total_news_investment_count


def get_project_urls(datalist):
    urls=""
    if(datalist!= None):
        for iteritem in datalist: #.iteritems():
            #print k,type(v),v
            for k,_v in iteritem.iteritems():
                if k == 'type' or k == 'name':
                    continue

                if(_v != ""):
                    #print 'v1',_v
                    _v = _v.encode("utf-8")
                    _v = _v.replace("\r"," ").replace("\n"," ")
                    _v= _v.replace("\t", " ")
                    urls+= _v + " "

    #print 'debug22',urls
    urls=urls.strip().lower()
    return urls

def get_leads_data_parser(datadict):
    content=""
    if(datadict != None):
        for k,v in datadict.iteritems():
            #print k,v,type(v)

            if(k=="abstract"):
                _abstract_in_json=v #datadict["abstract"]
                #print'_abstract_in_json', _abstract_in_json
                if(_abstract_in_json!=""):
                    _abstract_in_json=_abstract_in_json.encode("utf-8")
                    _abstract_in_json= stripprefix(_abstract_in_json)
                    sentlist=getallsents(_abstract_in_json)
                    realcontent =chr(4).join(sentlist)

                    content+=" "+realcontent 

            else:
                if( isinstance(v, list)):
                    for _subv in v:
                        if(_subv2 != ''):
                            _subv2 = _subv2.encode("utf-8")
                            #print 'subv2',_subv2 
                            content +=" " + _subv2;
                elif( isinstance(v, dict)):
                    for _k,_v in v.iteritems():
                        #print '2333',_k,_v,type(_v)
                        if( isinstance(_v, unicode)):
                            if(_v!= ''):
                                #print 'v in dict',_v
                                _v = _v.encode("utf-8")
                                content +=" " + _v;

    #print 'debug22',content 
    return content 

def get_leads_parser(datadict,content):
    founder=""
    if(datadict != None):
        for k,v in datadict.iteritems():
            vstr=""
            #print 'first level key:',k,type(v),v
            for _v in v:
                #print 'debug',k,'2th _v',_v,type(_v)
                #if(k.lower()=='stage' and isinstance(_v, list)):
                if(isinstance(_v, list)):
                    for _subv in _v:
                        #print k,'3th __subv v',_subv ,type(_subv )
                        for _subv2 in _subv:
                            if(_subv2 != ''):
                                _subv2 = _subv2.encode("utf-8")
                                vstr +=" " + _subv2;
                else:
                    if(_v != ""):
                        #print 'v1',_v,type(_v)
                        _v = _v.encode("utf-8")
                        vstr +=" " + _v;
                        #print 'v3331',_v,type(_v),vstr 
                        #print 'content',content
                        #print 'after encode ----v1',_v,content

            if(k.lower()=="founder"):
                founder+=vstr 
            else:
                content+=vstr 

    #print 'debug22',content 
    return content,founder

def get_crawled_leads(rescan=None):
    pid =0
    if(rescan==None):
    #if(1):
        pid = DataAccess_IR.get_last_crawled_leadsid()
        if(pid != 0):
            pid =(-1)*pid -120000000
            print 'pid begin', pid 


    ctime = str(time.strftime("%Y-%m-%d %H:%M:%S"))

    total_leads_crawled_count=0
    
    #try:
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_leads_crawled(pid)

            if results==None or len(results)==0:
                print 'get_crawled_leads no result',pid
                break

            print 'get_leads_crawled result len:',len(results),' pid :',pid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))
            #sql="SELECT id,title,`abstract`,city,`website`,`creationTime`,mark  FROM `mydb`.`project_leads` where id > "+str(pid)+" ORDER BY `id` LIMIT 500;"

            if results:
                con=None
                try:
                    for result in results:
                        pid = result[0]
                        normalized_pid=(-1)*(12000*10000+pid)


                        title = result[1]
                        if(title ==None or title ==""):
                            continue

                        title =title.encode('utf-8','ignore').strip().lower()
                        title = title.replace('\t',' ')
                        title =title.replace(" ",chr(6))
                        title =title.replace("'",chr(7))
                        title =title.replace("'"," ")

                        _exisited_leadsid = DataAccess_IR.get_leadsid_by_title(title,normalized_pid);
                        dupids=""
                        if(_exisited_leadsid != 0):
                            dupids = str(_exisited_leadsid )
                        else:
                            dupids = ""

                        #print 'dupids ', dupids,_exisited_leadsid  ,type(_exisited_leadsid),'>0',_exisited_leadsid != 0

                        mark = result[6]
                        #if(mark ==None):
                        #    mark = ""
                        #else:
                        #    mark =mark.encode('utf-8','ignore')
                        #    if(mark == 'chosen'):
                        #        if(_exisited_leadsid != 0):
                        #            DataAccess_IR.rm_project_for_diffrent_round(normalized_pid,dupids)
                        #            #print 'updated for dup'
                        #        continue

                        content=""
                        founderinfo=""
                        team_feature_type=""
                        team_feature_value=""
                        team_feature_dict=None

                        abstract = result[2]
                        #print 'title = result[1]',abstract 
                        if(abstract ==None):
                            abstract = ""
                        else:
                            abstract =abstract.encode('utf-8','ignore')
                            #print 'after encode title = result[1]',abstract 
                            #print 'debug-abstract',  abstract 

                            datadict= json.loads(abstract) 
                            try:
                                #homepage, description, stage, founder, fullname, phone, mail, address, history
                                content,founderinfo = get_leads_parser(datadict,content)

                                if(founderinfo != ""):
                                    team_feature_type,team_feature_value,team_feature_dict=team_feature_extractor(founderinfo)

                                #print 'debug333',content
                                #os._exit(1)
                                sentlist=getallsents(content)
                                #print 'sentlist', sentlist
                                content =chr(4).join(sentlist)
                                #print 'debug-content ',  content #,abstract 
                                #print 'debug-abstract ',  abstract 
                            except:
                                print 'json-data parse error',pid
                                #os._exit(1)

                        #print 'debug content',content
                        #print 'debug founder',founderinfo
                        #print 'debug---'
                        #os._exit(1)

                        city = result[3]
                        if(city ==None):
                            city = ""
                        else:
                            city =city.encode('utf-8','ignore')
                            content += " "+city

                        website = result[4]
                        if(website ==None):
                            website = ""
                        else:
                            website =website.encode('utf-8','ignore')
                            
                        url = website 

                        creationtime = result[5]
                        if(creationtime ==None ):
                            creationtime = ctime
                        else:
                            creationtime = str(creationtime).encode("utf-8")
                            
                        updatetime = creationtime 


                        title_cate_field=title + " "+TITLE_SPLIT

                        title_cate_field=title_cate_field.lower()

                        content_with_team=content.lower()+" "+CONTENT_SPLIT+founderinfo.lower() 

                        content_with_team=content_with_team.replace("\t",' ')

                        title_cate_field=title_cate_field.replace("'"," ")
                        content_with_team=content_with_team.replace("'"," ")

                        title_cate_field = title_cate_field.replace(" ", chr(5))
                        content_with_team=content_with_team.replace(" ",chr(5))

                        title_cate_field = title_cate_field.replace("\r", chr(5)).replace("\n", chr(5))
                        content_with_team=content_with_team.replace("\r", chr(5)).replace("\n", chr(5))

                        dedup=16
                        
                        forword_index_with_occurance_pos = forword_index_with_occurance_pos.replace("'","\\'")

                        title_cate_field=realtitle#.replace( "'","\\'")
                        content_with_team=realcontent.replace( "'","\\'")
                        title=title.replace( "'","\\'")

                        #termcount_in_content = int(math.log(2.0+1.0/(2.0+abs(termcount_in_content-100.0)),2)*10000)
    
                        querystr=""
                        keywordstr_=""
                        catestr=""
                        attributestr=""
                        fieldliststr=""
                        attach=""
                        termstr=""
                        status=-80000
                        projectlevel=CRAWLED_LEADS_NOT_SYNCED
                        total_leads_crawled_count+=1

                        DataAccess_IR.add_project_ir(normalized_pid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,creationtime,updatetime,keywordstr_,status,projectlevel,forword_index_with_occurance_pos,title_cate_field,content_with_team,termcount_in_realtitle,termcount_in_content,url,dupids,None,team_feature_type,team_feature_value )

                        #print 'debug',pid ,content_with_team,termcount_in_realtitle
                        #print 'termcount_in_content',termcount_in_content
                        #print 'forword_index_with_occurance_pos ',forword_index_with_occurance_pos 
                        #os._exit(1)


                finally:
                    pass
    #except:
    #    print 'fund error',pid

    print 'total_leads_crawled_count', total_leads_crawled_count



def get_investment():
    pid =0

    leadsid = DataAccess_IR.get_last_investment_id()
    if(leadsid != 0):
        leadsid=(-1)*leadsid-60000000
    pid=leadsid

    ctime = str(time.strftime("%Y-%m-%d %H:%M:%S"))

    total_investment_count=0
    
    #try:
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_investment(pid)

            if results==None or len(results)==0:
                print 'no result',pid
                break

            print 'get_investment result len:',len(results),' pid :',pid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))
            #sql="SELECT id,name,field,statge,`scale`,`fundName`,`creationTime` FROM `mydb`.`project_investment`  where id > "+str(pid)+" ORDER BY `id` LIMIT  50;"

            if results:
                con=None
                try:
                    for result in results:
                        pid = result[0]

                        name= result[1]
                        if(name==None or name==""):
                            #username=""
                            continue

                        name=name.encode('utf-8','ignore')
                        name=name.strip().strip('\t')

                        title=name
                        content=name

                        field,content=normalize_field(result[2],content)
    
                        stage,content=normalize_field(result[3],content)
                        scale,content=normalize_field(result[4],content)
                        fundname,content=normalize_field(result[5],content)
                        creationtime = result[6]
                        if(creationtime ==None ):
                            creationtime = ctime
                        else:
                            creationtime = str(creationtime).encode("utf-8")
                            
                        updatetime = creationtime 

                        title =title.replace(" ",chr(6))
                        title =title.replace("'",chr(7))

                        title = title.replace('\t',' ')
                        title =title.replace("'"," ")

                        title_cate_field=title + " "+TITLE_SPLIT

                        title_cate_field=title_cate_field.lower()

                        content_with_team=content.replace("\t",' ')
                        content_with_team=content_with_team.lower()

                        title_cate_field=title_cate_field.replace("'"," ")
                        content_with_team=content_with_team.replace("'"," ")

                        title_cate_field = title_cate_field.replace(" ", chr(5))
                        content_with_team=content_with_team.replace(" ",chr(5))

                        title_cate_field = title_cate_field.replace("\r", chr(5)).replace("\n", chr(5))
                        content_with_team=content_with_team.replace("\r", chr(5)).replace("\n", chr(5))

                        dedup=16
                        
                        title=title.replace( "'","\\'")

                        #termcount_in_content = int(math.log(2.0+1.0/(2.0+abs(termcount_in_content-100.0)),2)*10000)
    
                        normalized_pid=(-1)*(6000*10000+pid)
                        querystr=""
                        keywordstr_=""
                        catestr=""
                        attributestr=""
                        fieldliststr=""
                        attach=""
                        termstr=""
                        status=-30000
                        projectlevel=INVESTMENT
                        total_investment_count+=1

                        DataAccess_IR.add_project_ir(normalized_pid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,creationtime,updatetime,keywordstr_,status,projectlevel,forword_index_with_occurance_pos,title_cate_field,content_with_team,termcount_in_realtitle,termcount_in_content )

                        #print 'debug'


                finally:
                    pass
    #except:
    #    print 'fund error',pid

    print 'total_investment_count', total_investment_count


def get_investor():
    userid =0
    creationtime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    updatetime = str(time.strftime("%Y-%m-%d %H:%M:%S"))

    total_investor_count=0
    
    #try:
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_investor(userid)

            if results==None or len(results)==0:
                print 'no result',userid
                break

            print 'get_investor result len:',len(results),' userid :',userid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))
            #sql = " SELECT userid,username,name,company,phone,`email`,`weixin`,type    FROM `mydb`.`user` where userid > "+str(pid)+" ORDER BY `userId`    LIMIT 0,50;"

            if results:
                con=None
                try:
                    for result in results:
                        userid = result[0]

                        username= result[1]
                        #print 'username', username,result
                        #raw_input()
                        if(username==None or username==""):
                            username=""
                            #continue

                        type=result[7]
                        if(type==None):
                            #print 'type is none'
                            continue

                        if((type&2) !=2):
                            continue

                        username=username.encode('utf-8','ignore')

                        title=username
                        content=username

                        name,content=normalize_field(result[2],content)
                        if(name!=""):
                            title=name

                        title =title.replace(" ",chr(6))
                        title =title.replace("'",chr(7))
    
                        company,content=normalize_field(result[3],content)
                        phone,content=normalize_field(result[4],content)
                        email,content=normalize_field(result[5],content)
                        weixin,content=normalize_field(result[6],content)
                        financingRound,content=normalize_field(result[8],content)


                        currency=result[9]
                        if(currency):
                            if(currency&1==1):
                                content+="|人民币"
                            if(currency&2==2):
                                content+="|美元"

                        city,content=normalize_field(result[10],content)

                        userfav=get_user_fav(userid)
                        if(content!=""):
                            content+="|"+userfav
                        else:
                            content=userfav

                        fundid=result[17]
                        if(fundid!=358):
                            industry_query=get_user_industry_query(userid)
                            if(industry_query!=""):
                                content+=" "+industry_query

                            user_subed=get_user_subed(userid)
                            if(user_subed!=""):
                                content+=" "+user_subed


                        #print 'user_subed,',user_subed
                        #print 'industry_query,',industry_query
                        #os._exit(1)


                        searchtoken=result[15]
                        if(searchtoken==None):
                            searchtoken=""
                        else:
                            searchtoken=searchtoken.encode('utf-8','ignore')


                        personinfo=result[16]
                        if(personinfo==None):
                            personinfo=""
                        else:
                            if(personinfo!=""):
                                personinfo=personinfo.encode('utf-8','ignore').lower()
                                content +=" "+personinfo

                        position =result[18]
                        if(position == None):
                            position=""
                        else:
                            if(position!=""):
                                position=position.encode('utf-8','ignore').lower()
                                content +=" "+position


                        #print userid,userfav
                        #raw_input()

                        title = title.replace('\t',' ')
                        

                        title =title.replace("'"," ")

                        title_cate_field=title + " "+TITLE_SPLIT

                        if(searchtoken!=''):
                            searchtoken = searchtoken.replace('\t',' ')
                            title_cate_field += ' '+searchtoken

                        title_cate_field=title_cate_field.lower()

                        content_with_team=content.replace("\t",' ')
                        content_with_team=content_with_team.lower()

                        title_cate_field=title_cate_field.replace("'"," ")
                        content_with_team=content_with_team.replace("'"," ")

                        title_cate_field = title_cate_field.replace(" ", chr(5))
                        content_with_team=content_with_team.replace(" ",chr(5))

                        title_cate_field = title_cate_field.replace("\r", chr(5)).replace("\n", chr(5))
                        content_with_team=content_with_team.replace("\r", chr(5)).replace("\n", chr(5))

                        dedup=16
                        
                        keywordstr_=""
                        catestr=""
                        attributestr=""
                        fieldliststr=""
                        attach=""
                        termstr=""
                        status=-20000
                        projectlevel=INVESTOR#5000

                        total_investor_count+=1


                        if(phone!=""):
                            mask_phone=phone[0:len(phone)-3]+"***"
                            #print phone ,mask_phone
                            content_with_team=content_with_team.replace(phone,mask_phone)
                            #print content
                            #raw_input()

                        if(email!=""):
                            email=email.strip()
                            at_pos=email.find("@")
                            if(at_pos>0):
                                replace_email=email[0:at_pos]+chr(2)+"@"
                                #print 'replace_email', replace_email
                                mask_email="***" + replace_email[3:len(replace_email)]
                                #print mask_email,replace_email,content_with_team.find(replace_email)
                                #pos2=content_with_team.find(replace_email)
                                #pos3=content_with_team.find("zhenboran")+len("zhenboran")
                                #ch_=content_with_team[pos3:pos3+1]
                                #ch_3=content_with_team[pos3+1:pos3+2]
                                #print 'find pos',pos2,pos3,ch_,ch_==chr(3),ch_==chr(2),ch_3

                                content_with_team=content_with_team.replace(replace_email,mask_email)
                                #print content_with_team
                                #raw_input()

                        if(weixin!=""):
                            mask_weixin=weixin[0:len(weixin)-3]+"***"
                            content_with_team=content_with_team.replace(weixin,mask_weixin)

                        DataAccess_IR.add_project_ir(normalized_userid,title,catestr,attributestr,fieldliststr,termstr,querystr,attach,creationtime,updatetime,keywordstr_,status,projectlevel,forword_index_with_occurance_pos,title_cate_field,content_with_team,termcount_in_realtitle,termcount_in_content )

                        #print title_cate_field
                        #print content_with_team
                        #os._exit(1)

                finally:
                    pass
    #except:
    #    print 'fund error',userid

    print 'total_investor_count', total_investor_count


def get_fund():
    fundid =0
    creationtime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    updatetime = str(time.strftime("%Y-%m-%d %H:%M:%S"))
    
    #try:
    if(1):
        while(1):

            results = None
            results = DataAccess_IR.get_funds(fundid)

            if results==None or len(results)==0:
                print 'no result',fundid
                break

            print 'get_fund result len:',len(results),' fundid :',fundid ,str(time.strftime("%Y-%m-%d %H:%M:%S"))
            #sql = " SELECT fundid,name,englishname,nameshort,englishnameshort,city,address,comment FROM `mydb`.`fund` where fundid > "+str(pid)+"   ORDER BY `fundId`    LIMIT 0,50;"

            if results:
                con=None
                try:
                    for result in results:
                        fundid = result[0]

                        name= result[1]
                        if(name==None or name==""):
                            continue

                        name=name.encode('utf-8','ignore')

                        title=name
                        content=name

                        englishname,content=normalize_field(result[2],content)
                        nameshort,content=normalize_field(result[3],content)
                        if(nameshort!=""):
                            title=nameshort

                        title =title.replace(" ",chr(6))
                        title =title.replace("'",chr(7))

                        englishnameshort,content=normalize_field(result[4],content)
                        city,content=normalize_field(result[5],content)

                        address= result[6]
                        if(address!=None and address!=""):
                            address=address.encode('utf-8','ignore')

                            try:
                            #if(1):
                                address_list= json.loads(address) 
                                i=0
                                while(i<len(address_list)):
        
                                    _city=address_list[i]["city"]
                                    _address = address_list[i]["address"]

                                    _city=_city.encode("utf-8")
                                    if(_city!=""):
                                        content += " "+_city

                                    _address=_address.encode("utf-8")
                                    if(_address!=""):
                                        content += " "+_address
                                    i+=1

                            except:
                                   print 'address parser error',fundid


                        #comment,content=normalize_field(result[7],content)

                        comment = result[7]
                        if(comment !=None):
                            comment =comment.encode('utf-8','ignore')

                            sentlist=getallsents(comment)
                                
                            realcontent =chr(4).join(sentlist)
                            content+=" "+realcontent 
                            #print '3333debugcomments',fundid,realcontent, comment
                        else:
                            comment = ""

                        financingRound,content=normalize_field(result[8],content)

                        info = result[9]
                        if(info !=None):
                            info = info.encode('utf-8','ignore')
                            sentlist=getallsents(info )
                            realinfo =chr(4).join(sentlist)
                            content+=" "+realinfo 

                        isStrategy = result[10]
                        #print 'strategr---', isStrategy,(isStrategy == 1)
                        if(isStrategy == 1):
                            content+=chr(4)+" 战投 战略投资"

                        thirdboard = result[12]
                        #print 'strategr---', isStrategy,(isStrategy == 1)
                        if(thirdboard == 1):
                            content+=chr(4)+" 新三板"


                        fund_fav = get_fund_fav(fundid)
                        content+=chr(5)+fund_fav

                        title = title.replace('\t',' ')

                        title_cate_field=title + " "+TITLE_SPLIT
                        title_cate_field=title_cate_field.lower()

                        content_with_team=content.replace("\t",' ')


                        title_cate_field = title_cate_field.lower()
                        content_with_team=content_with_team.lower()

                        title_cate_field=title_cate_field.replace("'", " ")
                        content_with_team=content_with_team.replace("'", " ")

                        title_cate_field = title_cate_field.replace("\r", chr(5)).replace("\n", chr(5))
                        content_with_team=content_with_team.replace("\r", chr(5)).replace("\n", chr(5))


                        title_cate_field = title_cate_field.replace(" ", chr(5))
                        content_with_team=content_with_team.replace(" ",chr(5))

                        dedup=16
                        

                        #print 'debugcomments',fundid,forword_index_with_occurance_pos
                        #exit(1)
                        #os._exit(-1)

                finally:
                    pass
    #except:
    #    print 'fund error',fundid


def get_uname_by_id(userid):
    name=""
    results = DataAccess_IR.get_uname_by_id(userid)


    if results:
        for result in results:
            title = result[0].strip()
            if(title):
                title = title.replace('\t',' ')
                title = title.replace('\n',' ')
                title = title.encode('utf-8','ignore')
                name=title
            break

    return name


def get_cate_by_id(categoryid):
    cate=""
    results = DataAccess_IR.get_cate_by_id(categoryid)


    if results:
        for result in results:
            title = result[0].strip()
            if(title):
                title = title.replace('\t',' ')
                title = title.replace('\n',' ')
                title = title.encode('utf-8','ignore')
                cate=title
            break

    return cate


def get_agent_for_appdata():
    global dilimeter_list
    global dilimeter_dict

    total_num = 0
    category_num = 0 
    category_id = 0 


prj_tag={}
tag_init=0
phrase_inverted_dict=defaultdict(list)

def phrase_tag_init():
    global dilimeter_list
    global dilimeter_dict
    global prj_tag
    global prj_tag_list
    global tag_init
    global phrase_inverted_dict
    con=None
    dedup=16
    phrase_forward_dict=defaultdict(int)
    #phrase_forward_with_occur_dict=defaultdict(int)
    phrase_forward_with_occur_dict=defaultdict(int)
    if(tag_init==0):
        prj_tag_dict = get_all_tags(False)
        prj_tag_list = ' '.join(prj_tag_dict.keys())
        tagarr=prj_tag_list.split(' ')
        for t in tagarr:
            t=t.strip().strip('\t')
            if(len(t)>1):
                t=t.lower()
                prj_tag[t]=1

		title_cate_field=t+ chr(5) + TITLE_SPLIT
		title_cate_field=title_cate_field.strip()
		title_cate_field=title_cate_field.replace("\t",' ')
		title_cate_field=title_cate_field.lower()

		content_with_team=chr(5)
		content_with_team=content_with_team.replace("\t",' ')

		tag_dict,term_list=term_extract(title_cate_field,content_with_team,con,logger,dedup,cate_dict) 

		term_count=len(tag_dict)-1
		if(term_count==1):
		    #print 'only with len = 1',t
		    continue

		firstTwoKeys=''.join(term_list[:2])
		#print 'firstTwoKeys', firstTwoKeys
		remain_list=term_list[2:]
		#print 'remains',remain_list,type(remain_list)
		phrase_inverted_dict[firstTwoKeys].append(remain_list)

		#for k_with_occur in tag_with_occur:
		#    k=k_with_occur[0] 
		#    #count=k_with_occur[1] 
		#    phrase_forward_with_occur_dict[k]=k_with_occur[2:] 

		#for k,v in tag_dict.iteritems():
		#    if(k==TITLE_SPLIT_FILTER):
		#	continue
		#    phrase_inverted_dict[k][t]=term_count
		#    #print k,t
		#    #raw_input()
		#phrase_forward_dict[t]=term_count
		#print t,'dictlen',len(tag_dict)-1
        tag_init=1

    return



def GetPhraseSeg(termlist2seg):         
    results = []
    results_dict = {}

    #print 'len:',len(phrase_inverted_dict)
    #try:            
    if(1):
	termcount = len(termlist2seg)
	pos = 0;

	while (pos <= (termcount-2)):
	    tmpStartPos = pos;
	    if (pos + 1 <= termcount):
		tmpstr = ''.join(termlist2seg[pos:(pos+2)])
		#print 'tmpstr ', tmpstr
		pos =pos + 2;
	       
		isFound = False
		if(phrase_inverted_dict.has_key(tmpstr)):
		    arrs = phrase_inverted_dict[tmpstr]  
		    
		    FoundItem = None       
		    matchLen = 0;         
		    for item in arrs:
			#item =word
			#_type =word_type[1]
			lenK = len(item)
			if(pos + lenK > termcount):
			    continue;

			candidateStr = ''.join(termlist2seg[pos:(pos+lenK)])
			targetStr=''.join(item)

			if (candidateStr == targetStr):

			    isFound = True;
			    if( FoundItem == None or ( len(FoundItem)<(len(item)+1))):
				item = "".join(termlist2seg[tmpStartPos:(pos+lenK)])

				matchLen = lenK;
				FoundItem = item;

			    #elif( len(FoundItem.restword)>(len(item.restword)+2)):
			    #    #item.restword = str[tmpStartPos:(pos - tmpStartPos)]                               
			    #    item.restword = str[tmpStartPos:(pos)]                               
			    #    FoundItem = item;

			    #results.append(FoundItem)
			    #results.append(str.Substring(tmpStartPos, pos - tmpStartPos));

		    if(isFound):
			pos =pos + matchLen;

			#print 'found',FoundItem

			if(not results_dict.has_key(FoundItem)):
			    results_dict[FoundItem]=1
			    results.append(FoundItem)

		if(not isFound):
		    #since we add 2 before,just move back
		    pos =pos - 1;
	    else:                 
		pos=pos+1
		if (pos == termcount):
		    break;

    #except:
    #    print 'TeamClassifySegStr-sys[0]+',sys.exc_info()[0]
	pass  

    return results


if __name__ == "__main__":
    phrase_tag_init()

    termlist2seg=["3d","打印",'精准','营销']
    result=GetPhraseSeg(termlist2seg)
    print result
    for r in result:
	print 'phrase',r


