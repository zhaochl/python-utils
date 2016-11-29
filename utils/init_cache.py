#!/usr/bin/env python
# coding=utf-8
from cache_util import *
from data_loader import *
from pdb import *
from constant import *
from termclient_util import *
from up_utils import *
from date_util import *

def init_action_weight_decay(debug=True):
    week_total = 53
    if debug:
        week_total = 53
    all_action_weight_decay = {}
    for _action,_weight in const_action_weight.iteritems():
        action_weight_decay_pow_arr = []
        action_weight_decay_pow = _weight
        action_weight_decay = const_action_weight_decay[_action] 
        for i in range(week_total):
            if i==0:
                action_weight_decay_pow = _weight
            else:
                action_weight_decay_pow *=  action_weight_decay
            action_weight_decay_pow_arr.append(action_weight_decay_pow)
        all_action_weight_decay[_action] = action_weight_decay_pow_arr
    
    return all_action_weight_decay

def calc_action_weight(type,creationTime,debug=True):
    
    action_weight_decay = CR(init_action_weight_decay,debug)
    # add action_weight
    action_weight = 0.0
    past_week = calc_past_week(creationTime)
    action_weight_decay_pow_arr = action_weight_decay[type]
    #print type,creationTime,past_week,action_weight_decay_pow_arr
    action_weight = action_weight_decay_pow_arr[past_week]
    return action_weight

"""
investorId:[investorId,userId,fundId]
"""
def init_investor_info(debug=True):
    info = {}
    limit =-1
    if debug:
        limit = debug_limit
    results = load_investor_info_data_dict(limit)
    if results!=None and len(results)>0:
        info = results
    return info

"""
全部非以太的userId:fundId
"""
def init_user_data_dict(debug=True):
    yitai_user = {}
    info = {}
    limit =-1
    if debug:
        limit = debug_limit
    results = load_user_data_dict(limit)
    if results!=None and len(results)>0:
        #for r in results:
        for userId,r in results.iteritems():
            userId = int(r[0])
            fundId = int(r[1])
            userName = r[2]
            name = r[3]
            company = r[4]
            type = int(r[5])
            #is localhost user,continue
            if type&1 == 1:
                yitai_user[userId] = name
                continue
            if fundId==0:
                continue
            info[userId] = fundId
    return info,yitai_user

def init_project_tab_data(debug=True):
    all_project_cate_term = {}
    limit =-1
    if debug:
        limit = debug_limit
    results = load_project_tab_data(limit)
    if results!=None and len(results)>0:
        for r in results:
            pid = r[0]
            projectId = int(r[1])
            query_2_index = r[2]
            qarr = query_2_index.strip('\t').split('\t')
            tag = ''
            weight = 0.0
            last_tag =''
            project_cate_term = {}
            t_cate_dict = {}
            k_term_dict ={}
            #print pid
            for _index,_val in enumerate(qarr):
                #print _val   
                if _index &1 == 0:
                    _val = _val.replace('T_','c_')
                    _val = _val.replace('t_','c_')
                    last_tag = _val
                    if _val.find('_')!=-1:
                        if _val.find('c_')!=-1:
                            t_cate_dict[_val] = 0
                    else:
                        k_term_dict['k_'+_val] =0
                else:
                    weight = float(_val)
                    if t_cate_dict.has_key(last_tag):
                        t_cate_dict[last_tag] = weight
                    elif k_term_dict.has_key('k_'+last_tag):
                        k_term_dict['k_'+last_tag] = weight
            #print t_cate_dict
            #print k_term_dict
            project_cate_term['cate'] = t_cate_dict
            project_cate_term['term'] = k_term_dict
            all_project_cate_term[projectId] = project_cate_term
    return all_project_cate_term

def init_fund_cate_dict(debug=True):
    all_fund_field_dict = {}
    limit =-1
    if debug:
        limit = debug_limit
    results = load_fund_sector_data(limit)
    if results!=None and len(results)>0:
        for r in results:
            sectorId = r[0]
            fundId = r[1]
            sector = r[2]
            sector = 'b_'+sector
            preference = r[3]
            if preference==0:
                continue
            if not all_fund_field_dict.has_key(fundId):
                all_fund_field_dict[fundId] = {sector:preference}
            else:
                _old_data = all_fund_field_dict[fundId]
                if not _old_data.has_key(sector):
                    _old_data[sector] = preference
                all_fund_field_dict[fundId] = _old_data
    return all_fund_field_dict

def init_user_cate_dict(debug=True):
    all_user_field_dict = {}
    limit =-1
    if debug:
        limit = debug_limit
    results = load_user_sector_data(limit)
    if results!=None and len(results)>0:
        for r in results:
            sectorId = r[0]
            userId = r[1]
            sector = r[2]
            sector = 'b_'+sector
            sector = sector.lower()
            capability = r[3]
            preference = r[4]
            weight = preference+capability
            
            #delete
            if weight <= 50:
                continue

            if not all_user_field_dict.has_key(userId):
                all_user_field_dict[userId] = {sector:weight}
            else:
                _old_data = all_user_field_dict[userId]
                if not _old_data.has_key(sector):
                    _old_data[sector] = weight
                all_user_field_dict[userId] = _old_data
    return all_user_field_dict

def init_investor_app_log(debug=True):
    user_project_action_dict = {}
    recent_day = 90
    if debug:
        recent_day = debug_day
    results = load_investor_app_log_data(recent_day)  
    #print len(results)
    #-add decay
    user_info,yitai_user = CR(init_user_data_dict,debug)
    if results!=None and len(results)>0:
        for r in results:
            logId = r[0]
            userId = int(r[1])
            projectId = int(r[2])
            type = r[3].encode('utf8','ignore')
            subtype = r[4]
            creationTime = str(r[6])
            first = r[5]
            if first!=1:
                continue
            # check yitai_user
            if yitai_user.has_key(userId):
                continue
            action_weight = 0
            if const_action_weight.has_key(type):
                #action_weight = const_action_weight[type]
                action_weight = calc_action_weight(type,creationTime)
            else:
                continue
            
            if not user_project_action_dict.has_key(userId):
                user_project_action_dict[userId] = {projectId:action_weight}
            else:
                _old_data = user_project_action_dict[userId]
                if not _old_data.has_key(projectId):
                    _old_data[projectId] = action_weight
                else:
                    _old_data[projectId] += action_weight
    return user_project_action_dict

def init_search_query_log(debug=True):
    user_term_dict = {}

    user_query_dict = {}
    recent_day = 90
    if debug:
        recent_day = debug_day
    results = load_search_query_log_data(recent_day)
    
    user_info,yitai_user = CR(init_user_data_dict,debug)
    #print len(results)
    if results!=None and len(results)>0:
        for r in results:
            logId = r[0]
            userId = int(r[1])
            platform = r[2]
            query = r[3].encode('utf8','ignore')
            #query = r[3]
            sessionEnd = r[4]
            isIndustry = r[5]
            creationTime = str(r[6])
            creationTime_ymd_arr = creationTime.split(' ')
            creationTime_ymd = creationTime_ymd_arr[0]
            #print creationTime_ymd
            if platform=='admin':
                continue
            # check yitai_user
            if yitai_user.has_key(userId):
                continue
            #if isIndustry !=-1024:
            #    continue
            if len(query)<=3:
                continue
            # add action_weight
            action_weight = calc_action_weight('query',creationTime)
            
            query = query.replace(' ','').replace('\'','').replace('\"','').lower()
            query_ymd = query + chr(5)+creationTime_ymd
            if not user_query_dict.has_key(userId):
                user_query_dict[userId]=  {query_ymd:action_weight}
            else:
                _old_data = user_query_dict[userId]
                if not _old_data.has_key(query_ymd):
                    _old_data[query_ymd] = action_weight
                else:
                    pass
                    #_old_data[query_ymd] = action_weight
                user_query_dict[userId] = _old_data
    #if
    #print user_query_dict
    #set_trace()
    for _uid,_query_count_dict in user_query_dict.iteritems():
        _uid_term_count_dict = {}
        for _query_ymd,_count in _query_count_dict.iteritems():
            _query_ymd_arr = _query_ymd.split(chr(5))
            _query = _query_ymd_arr[0]
            terms = splite_term(_query)
            for term in terms:
                if len(term)<=3:
                    continue
                if not _uid_term_count_dict.has_key(term):
                    _uid_term_count_dict[term] = _count
                else:
                    _uid_term_count_dict[term] += _count
            #--add _query
            if not _uid_term_count_dict.has_key(_query):
                _uid_term_count_dict[_query] = _count
        _uid_term_count_dict_tmp = sorted(_uid_term_count_dict.items(), lambda x, y: cmp((x[1]), (y[1])), reverse=True)[0:100]
        _uid_term_count_dict_sort = {}
        for __k,__v in _uid_term_count_dict_tmp:
            _uid_term_count_dict_sort['q_'+str(__k).lower()] = format_float(__v)
        user_term_dict[_uid] = _uid_term_count_dict_sort
    return user_term_dict

def init_user_project_meeting(debug):
    user_project_meeting ={}
    limit =-1
    if debug:
        #limit = debug_limit
        limit = -1
    #all_investor_info = {}
    #all_investor_info = CR(init_investor_info,False)
    #print all_investor_info
    
    user_info,yitai_user = CR(init_user_data_dict,debug)
    results = load_meeting_data(limit)
    if results!=None and len(results)>0:
        for r in results:
            meetingId = r[0]
            #investorId = int(r[1])
            userId = int(r[1])
            projectId = int(r[2])
            status = r[3]
            creationTime = str(r[4])
            #if status=='canceled':
            if status!='online':
                continue
            if creationTime<'2016-01-01 00:00:00':
                continue
            #[infoId,userId,fundId]
            #investor_info = all_investor_info[investorId]
            #userId = investor_info[1]
            #print userId
            
            # add action_weight
            action_weight = calc_action_weight('meeting',creationTime)
            if not user_project_meeting.has_key(userId):
                user_project_meeting[userId] = {projectId:action_weight}
            else:
                _old_data = user_project_meeting[userId]
                if not _old_data.has_key(projectId):
                    _old_data[projectId] = action_weight
                else:
                    _old_data[projectId] += action_weight
    return user_project_meeting

def test(debug):
    #t= init_investor_info(debug)
    #t= init_project_tab_data(debug)
    #t= init_search_query_log(debug)
    #print t
    #t = init_user_project_meeting(debug)
    #print t
    t = init_investor_app_log(debug)
    #t= init_user_cate_dict()
    #print t[352]
    #t = init_action_weight_decay(debug)
    print t
if __name__=='__main__':
    #debug = True
    debug = False
    test(debug)
