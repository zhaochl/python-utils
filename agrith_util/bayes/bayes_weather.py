#!/usr/bin/env python
# coding=utf-8
from pdb import *

def load_data():
    #Outlook-Temperature-Humidity-Wind-status
    l = [('Sunny','Hot','High','Weak','No'),
    ('Sunny','Hot','High','Strong','No'),
    ('Overcast','Hot','High','Weak','Yes'),
    ('Rain','Mild','High','Weak','Yes'),
    ('Rain','Cool','Normal','Weak','Yes'),
    ('Rain','Cool','Normal','Strong','No'),
    ('Overcast','Cool','Normal','Strong','Yes'),
    ('Sunny','Mild','High','Weak','No'),
    ('Sunny','Cool','Normal','Weak','Yes'),
    ('Rain','Mild','Normal','Weak','Yes'),
    ('Sunny','Mild','Normal','Strong','Yes'),
    ('Overcast','Mild','High','Strong','Yes'),
    ('Overcast','Hot','Normal','Weak','Yes'),
    ('Rain','Mild','High','Strong','No')]

    return l
def update_data_count(data_count,i,k,type):
    data = data_count[i]
    if data.has_key(type):
        d = data[type]
        if not d.has_key(k):
            d[k] = 1
        else:
            d[k]+=1
        data[type]=d
    else:
        data[type] = {k:1}
    data_count[i] = data
    return data_count

def process():
    data_count = []
    for i in range(4):
        data_count.append({})
    result = load_data()
    status_count = {}
    status_total = 0
    for index,r in enumerate(list(result)):
        
        Outlook = r[0]
        Temperature = r[1]
        Humidity = r[2]
        Wind = r[3]
        status = r[4]
        #print status
        if not status_count.has_key(status):
            status_count[status] =1
        else:
            status_count[status] +=1
        #set_trace()
        for i in range(4):
            update_data_count(data_count,i,r[i],status)
        status_total+=1
    status_percent = {}
    for status,count in status_count.iteritems():
        status_percent[status] = float(count)/float(status_total)
    print status_percent

    data_percent_list =[]
    for item in data_count:
        data_percent_obj = {}
        for status,type_count_dict in item.iteritems():
            data_percent_obj_status = {}
            for type,count in type_count_dict.iteritems():
                data_percent_obj_status[type] = float(count)/float(status_count[status])
            data_percent_obj[status] = data_percent_obj_status
        data_percent_list.append(data_percent_obj)
    
    print data_percent_list
    #return data_percent_list,status_percent
    case = ('Sunny','Cool','High','Strong')
    print case
    case_status_percent_dict ={}
    for status,percent in status_percent.iteritems():
        case_status_percent = percent
        #set_trace()
        for i,type in enumerate(case):
            data_obj = data_percent_list[i]
            type_obj = data_obj[status]
            case_status_percent *= type_obj[type] 
        case_status_percent_dict[status] = case_status_percent
    
    print case_status_percent_dict
if __name__=='__main__':
    t = process()
    print t
