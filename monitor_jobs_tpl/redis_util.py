#!/usr/bin/python
# -*- coding: utf-8 -*-
import redis
import datetime
import json
#global rinst
def init_redis():
    #rInst = redis.StrictRedis(host='localhost', port=6379, db=0)
    rInst = redis.StrictRedis(host='localhost', port=6379, db=0)
    return rInst
#unuse
def init_redis_test():
    #rInst = redis.StrictRedis(host='localhost', port=6379, db=0)
    rInst = redis.StrictRedis(host='localhost', port=6380, db=0)
    return rInst
#--------for verify itemCF------------------
def set_list_verify(key,val):
    rInst = init_redis()
    #rInst.set('verify:list:'+key,val)
    rInst.rpush('verify:'+key,val)
def del_list_key_verify(key):
    rInst = init_redis()
    if rInst.exists('verify:'+key):
        rInst.delete('verify:'+key)
def get_list_verify(key):
    _result = []
    rInst = init_redis()
    if rInst.exists('verify:'+key):
        _result = rInst.lrange('verify:'+key,0,-1)
        #print _result
    return _result
#---------------end verify-----------------------
def get_break_point(key):
    _result=0
    rInst = init_redis()
    key = 'string:'+key
    if rInst.exists(key):
        _result = int(rInst.get(key))
    else:
        rInst.set(key,0)
    return _result
def set_break_point(key,value):
    key = 'string:'+key
    rInst=init_redis()
    rInst.set(key,value)
#---------add by zcl at 2016.1.21
def get_json_to_dict(type,id):
    _result=None
    rInst = init_redis()
    key = 'json:'+type+':'+str(id)
    if rInst.exists(key):
        _result_tmp = rInst.get(key)
        if _result_tmp!=None:
            _result = json.loads(_result_tmp)
    return _result
def set_json_from_dict(type,id,dict):
    key = 'json:'+type+':'+str(id)
    rInst=init_redis()
    rInst.set(key,json.dumps(dict))
#---------------------------
def get_json_to_hash_hash(type):
    _result=None
    rInst = init_redis()
    key = 'json:'+type
    if rInst.exists(key):
        _result_tmp = rInst.get(key)
        if _result_tmp!=None:
            _result = json.loads(_result_tmp)
    return _result
def set_json_from_hash_hash(type,dict):
    key = 'json:'+type
    rInst=init_redis()
    rInst.set(key,json.dumps(dict))

#---------add by zcl at 2016.1.14
def get_rec_results_json_to_dict(uid):
    _result=None
    rInst = init_redis()
    key = 'json:rec_results:'+str(uid)
    if rInst.exists(key):
        _result_tmp = rInst.get(key)
        if _result_tmp!=None:
            _result = json.loads(_result_tmp)
    return _result
def set_rec_results_json_from_dict(uid,dict):
    key = 'json:rec_results:'+str(uid)
    rInst=init_redis()
    rInst.set(key,json.dumps(dict))

#----------- add by zcl at 2016.1.19
def get_item_rec_results_json_to_dict(pid):
    _result=None
    rInst = init_redis()
    key = 'json:item_rec_results:'+str(pid)
    if rInst.exists(key):
        _result_tmp = rInst.get(key)
        if _result_tmp!=None:
            _result = json.loads(_result_tmp)
    return _result
'''
rec result: uid1:{pid001:0.8,pid002:0.6}
save to json key:uid1,val:{pid001:0.8,..}
'''
def set_item_rec_results_json_from_dict(pid,dict):
    key = 'json:item_rec_results:'+str(pid)
    rInst=init_redis()
    rInst.set(key,json.dumps(dict))
#---------------
def get_user_projects_total_score_hash_one(uid,pid):
    rInst=init_redis()
    _hkey = 'hash:projectx_score:uid'+str(uid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = pid
    _result =0
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_projectkey)
    else:
        rInst.hset(_hkey,_projectkey,0)
        _result = 0
    if _result ==None:
        _result =0
    return _result
def get_user_projects_total_score_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:projectx_score:uid'+str(uid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
def set_user_projects_total_score_hash(uid,pid,score):
    rInst=init_redis()
    _hkey = 'hash:projectx_score:uid'+str(uid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = pid
    rInst.hset(_hkey,_projectkey,score)
#------------------------log detail----------------------------
def get_user_last_project_logdetail_hash_one(uid,pid):
    rInst=init_redis()
    _hkey = 'hash:projectx_logdetal:uid'+str(uid)+'LastLogDetailHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = pid
    _result =None
    #print rInst.exists(_hkey),rInst.exists(int(_hkey)),rInst.exists(str(_hkey))
    print rInst.exists(_hkey),'-',rInst.exists(str(_hkey))
    if rInst.exists(_hkey):
        _result = rInst.hget(str(_hkey),str(_projectkey))
    else:
        rInst.hset(_hkey,_projectkey,0)
        _result = 0
    if _result ==None:
        _result =0
    return _result
def get_user_last_project_logdetail_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:projectx_logdetal:uid'+str(uid)+'LastLogDetailHash'
    #_projectkey = 'pid'+str(pid)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
def set_user_last_project_logdetail_hash(uid,pid,logdetail):
    rInst=init_redis()
    _hkey = 'hash:projectx_logdetal:uid'+str(uid)+'LastLogDetailHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = pid
    rInst.hset(_hkey,_projectkey,logdetail)

#------------------------rec-user-project-score----------------
def get_rec_user_projects_total_score_hash_one(uid,pid):
    rInst=init_redis()
    _hkey = 'hash:rec_projectx_score:uid'+str(uid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = pid
    _result =0
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_projectkey)
    else:
        rInst.hset(_hkey,_projectkey,0)
        _result = 0
    if _result ==None:
        _result =0
    return _result
def get_rec_user_projects_total_score_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:rec_projectx_score:uid'+str(uid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
def set_rec_user_projects_total_score_hash(uid,pid,score):
    rInst=init_redis()
    _hkey = 'hash:rec_projectx_score:uid'+str(uid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = pid
    rInst.hset(_hkey,_projectkey,score)
#-----------------------------

def get_list(key):
    _result = []
    rInst = init_redis()
    if rInst.exists('list:'+key):
        _result = rInst.lrange('list:'+key,0,-1)
        #print _result
    return _result
def set_list(key,val):
    rInst = init_redis()
    #rInst.set('list:'+key,val)
    rInst.rpush('list:'+key,val)
def del_list_key(key):
    rInst = init_redis()
    if rInst.exists('list:'+key):
        rInst.delete('list:'+key)
#--neighbors topk
def get_user_NB_topk_hash_one(uid,uidx):
    rInst=init_redis()
    _hkey = 'hash:userx_nb_topk:uid'+str(uid)+'NBTopKHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = uidx
    _result =0
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_projectkey)
    else:
        rInst.hset(_hkey,_projectkey,0)
        _result = 0
    return _result
def get_user_NB_topk_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:userx_nb_topk:uid'+str(uid)+'NBTopKHash'
    #_projectkey = 'pid'+str(pid)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
def set_user_NB_topk_hash(uid,uid2,sim):
    rInst=init_redis()
    _hkey = 'hash:userx_nb_topk:uid'+str(uid)+'NBTopKHash'
    _projectkey = uid2
    rInst.hset(_hkey,_projectkey,sim)

#----------------start project
"""
copied from user,u->p

"""
#--score
def get_project_users_total_score_hash_one(pid,uid):
    rInst=init_redis()
    _hkey = 'hash:userx_score:pid'+str(pid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = uid
    _result =0
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_projectkey)
    else:
        rInst.hset(_hkey,_projectkey,0)
        _result = 0
    if _result ==None:
        _result =0
    return _result
def get_project_users_total_score_hash_all(pid):
    rInst=init_redis()
    _hkey = 'hash:userx_score:pid'+str(pid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
def set_project_users_total_score_hash(pid,uid,score):
    rInst=init_redis()
    _hkey = 'hash:userx_score:pid'+str(pid)+'ProjectsScoreHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = uid
    rInst.hset(_hkey,_projectkey,score)
#----NBTopKHash
def get_project_NB_topk_hash_one(uid,uidx):
    rInst=init_redis()
    _hkey = 'hash:projectx_nb_topk:uid'+str(uid)+'NBTopKHash'
    #_projectkey = 'pid'+str(pid)
    _projectkey = uidx
    _result =0
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_projectkey)
    else:
        rInst.hset(_hkey,_projectkey,0)
        _result = 0
    return _result

def get_project_NB_topk_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:projectx_nb_topk:uid'+str(uid)+'NBTopKHash'
    #_projectkey = 'pid'+str(pid)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result

def set_project_NB_topk_hash(uid,uid2,sim):
    rInst=init_redis()
    _hkey = 'hash:projectx_nb_topk:uid'+str(uid)+'NBTopKHash'
    _projectkey = uid2
    rInst.hset(_hkey,_projectkey,sim)

"""
copied from user,u->p
get project1 all projectx sim hash one
u1 {'u2':0.01,'u3':0.02}
"""
def get_project_sim_hash_one(uid,uidx):
    rInst=init_redis()
    _hkey = 'hash:projectx_sim:pid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _uidxkey = uidx
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_uidxkey)
        #if _result=='None' or _result==None:
        #    _result=0
    #else:
        #rInst.hset(_hkey,_uidxkey,0)
        #_result = 0
    return _result
"""

copied from user,u->p
get project1 all projects sim hash all
u1 {'u2':0.01,'u3':0.02}
"""
def get_project_sim_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:projectx_sim:pid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
"""
copied from user,u->p
"""
def set_project_sim_hash(uid,uidx,sim):
    rInst=init_redis()
    _hkey = 'hash:projectx_sim:pid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _uidxkey = uidx
    if sim!=None and sim !='None' and sim !=0:
        rInst.hset(_hkey,_uidxkey,sim)

#--------------------end project
"""
get user1 all users sim hash one
u1 {'u2':0.01,'u3':0.02}
"""
def get_user_sim_hash_one(uid,uidx):
    rInst=init_redis()
    _hkey = 'hash:userx_sim:uid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _uidxkey = uidx
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_uidxkey)
        #if _result=='None' or _result==None:
        #    _result=0
    #else:
        #rInst.hset(_hkey,_uidxkey,0)
        #_result = 0
    return _result
"""
get user1 all users sim hash all
u1 {'u2':0.01,'u3':0.02}
"""
def get_user_sim_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:userx_sim:uid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
def set_user_sim_hash(uid,uidx,sim):
    rInst=init_redis()
    _hkey = 'hash:userx_sim:uid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _uidxkey = uidx
    if sim!=None and sim !='None' and sim !=0:
        rInst.hset(_hkey,_uidxkey,sim)
#-----------------------
# add by chunliang at 2016.1.13
#
#------------------------
"""
get user1 all users sim hash one
u1 {'u2':0.01,'u3':0.02}
"""
def get_user_sim_date_hash_one(uid,uidx):
    rInst=init_redis()
    _hkey = 'hash:userx_sim_date:uid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _uidxkey = uidx
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hget(_hkey,_uidxkey)
        #if _result=='None' or _result==None:
        #    _result=0
    #else:
        #rInst.hset(_hkey,_uidxkey,0)
        #_result = 0
    return _result
"""
get user1 all users sim hash all
u1 {'u2':0.01,'u3':0.02}
"""
def get_user_sim_date_hash_all(uid):
    rInst=init_redis()
    _hkey = 'hash:userx_sim_date:uid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _result =None
    if rInst.exists(_hkey):
        _result = rInst.hgetall(_hkey)
    return _result
def set_user_sim_date_hash(uid,uidx,sim):
    rInst=init_redis()
    _hkey = 'hash:userx_sim_date:uid'+str(uid)+'SimHash'
    #_uidxkey = 'sim'+str(uidx)
    _uidxkey = uidx
    if sim!=None and sim !='None' and sim !=0:
        rInst.hset(_hkey,_uidxkey,sim)
#--------------------add end-----------------
"""
rInst = init_redis()
rInst.set('foo', 'bar')
#True
res=rInst.get('foo')
#'bar'
print res
data=r.lrange('list:logstash_www',0,-1)
data=r.set('list:logstash_www1',data)
if rInst.exists('uid101ProjectScoreHash'):
    print 'yes'
    res = rInst.hget('uid101ProjectScoreHash','pid001')
    print 'res:',res
else:
    rInst.hset('uid101ProjectScoreHash','pid001','25')
    print 'no'
"""
if __name__=='__main__':
    '''
    print __file__
    print __name__
    print 'this is redis_util main.'
    rInst = init_redis()
    plist = rInst.hgetall('hash:uid10621ProjectsScoreHash')
    print plist
    simHash = get_user_sim_hash_all(27491)
    print '--simHash---'
    print simHash
    simHash  = get_user_sim_hash_one(27491,19425)
    print 's1:',simHash
    simHash  = get_user_sim_hash_one('27491','19425')
    print 's2:',simHash
    simHash  = get_user_sim_hash_one('27491',19425)
    print 's3:',simHash
    key='testList'
    data = ['t1','t2']
    set_list(key,' '.join(data))#bad
    rInst = init_redis()
    _result = get_list(key)
    print key,_result
    #rInst.shutdown() shut redis-server
    #rinst.close error
    #rInst.disconnect()
    #rInst.exit()

    #----test set_user_sim_date_hash --
    _today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    set_user_sim_date_hash(1,1,_today)
    sim_date = get_user_sim_date_hash_one(1,1)
    print sim_date
    #-------------test set_user_last_project_logdetail_hash-
    print '---fk---'
    set_user_last_project_logdetail_hash(1,1,'fk')
    t= get_user_last_project_logdetail_hash_one(1,1)
    print t

    set_user_last_project_logdetail_hash(1,1,'fk2')
    t= get_user_last_project_logdetail_hash_one(1,1)
    print t
    user_rec_dict = {'1':0.1,'2':0.05}
    set_rec_results_json_from_dict(1,user_rec_dict)
    t = get_rec_results_json_to_dict(1)
    print t
    '''
       
    #key ='item_rec_project_list'
    #item_rec_project_list = [1,2,3]
    #set_json_from_dict(key,item_rec_project_list)
