#!/bin/python
import json
import os
def write_file(file_name,str):
    pos = file_name.rfind('/')
    dir_path = file_name[:pos]
    if not os.path.exists(dir_path):
        #os.mkdir(dir_path)
        os.makedirs(dir_path)
        print 'mkdir '+dir_path+' ok'
    wordF= file( file_name,'w')
    wordF.write('%s' %(str))
    wordF.close()

def append_file(file_name,str):
    wordF= file( file_name,'a')
    wordF.write('%s' %(str))
    wordF.close()

def writefile_int(file_name,iValue):
    wordF= file( file_name,'w')
    wordF.write('%d' %(iValue))
    wordF.close()

def read_file(file_name):
    if not os.path.exists(file_name):
        return ""
    singleFile= file( file_name,'r')
    singleFile.seek(0)
    fContent = singleFile.read()
    singleFile.close()
    return fContent
def read_file_line(file_name):
    file_doc = open(file_name ,'rb')
    lines = file_doc.readlines()
    file_doc.close()
    line_data=[]
    for line in lines:
        line = line.replace('\n','')
        line_data.append(line)
    return line_data

"""
line like 
a,1,2,3
b,2,4,1
return [[a,1,2,3],[b,2,4,1]]
"""
def read_csv_to_list(csv_file):
    result = []
    try:
        f =  open(csv_file,'rb')
        lines = f.readlines()
        for line in lines:
            line = line.replace('\n','')
            line_arr = line.split(',')
            result.append(line_arr)
    except:
        print 'read file error'
        exit(1)
    return result
def set_json_to_dict_file(file_name,dict):
    write_file(file_name,json.dumps(dict))
def get_json_from_dict_file(file_name):
    d={}
    str = read_file(file_name)
    d = json.loads(str)
    return d
if __name__=='__main__':
    d ={'a':1}
    f = 'dat1/1.json'
    #set_json_to_dict_file(f,d)
    t = get_json_from_dict_file(f)
    #print t
    t = read_csv_to_list('_demo.csv')
    print t
