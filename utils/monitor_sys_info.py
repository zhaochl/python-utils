#!/usr/bin/env python
# coding=utf-8
import time,os
from mail_util import *
"""
by zcl at 2016
"""
def get_mem(): 
    percent =0.0
    with open('/proc/meminfo') as f: 
        total = int(f.readline().split()[1]) 
        free = int(f.readline().split()[1]) 
        buffers = int(f.readline().split()[1]) 
        cache = int(f.readline().split()[1]) 
        mem_use = total-free-buffers-cache 
        mem_use_g = mem_use/1024
        #print mem_use_g
        #time.sleep(1)
        percent = float(mem_use_g)/4096.0
    return strfromfloat(percent)
def percent2decimal(x):
    tmp = str(x).strip().strip('%')
    return float(tmp)/100
def get_disk():
    dis_stats = os.popen("df -lh|tail -n2|awk '{print $5}'|head -n1").readlines()
    disk_info = str(dis_stats[0])
    return percent2decimal(disk_info)

def read_cpu_usage():  
    """Read the current system cpu usage from /proc/stat.""" 
    cpu_mutil_core_infos = []
    try:  
        fd = open("/proc/stat", 'r')  
        num =1
        lines = None
        while True:
            lines = fd.readlines()  
            if not lines:
                break
            for line in lines:  
                l = line.split()  
                if len(l) < 5:  
                    continue 
                if l[0].startswith('cpu'):
                    cpu_mutil_core_infos.append(l)
            num+=1
            #if(num==2):
            #   break
    finally:  
        if fd:  
            fd.close()  
    return cpu_mutil_core_infos 
   
def calc_cpu_usage(cpustr,cpustr2):  
    """ 
    get cpu avg used by percent 
    """ 
    #cpustr = read_cpu_usage()  
    if not cpustr:  
        return 0 
    #cpu usage=[(user_2 +sys_2+nice_2) - (user_1 + sys_1+nice_1)]/(total_2 - total_1)*100  
    usni1=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[5])+long(cpustr[6])+long(cpustr[7])+long(cpustr[4])  
    usn1=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])  
    #usni1=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])+long(cpustr[4])  
    # self.sleep=2  
    time.sleep(2)
    cpustr=cpustr2  
    if not cpustr2:  
        return 0 
    usni2=long(cpustr[1])+long(cpustr[2])+float(cpustr[3])+long(cpustr[5])+long(cpustr[6])+long(cpustr[7])+long(cpustr[4])  
    usn2=long(cpustr[1])+long(cpustr[2])+long(cpustr[3])  
    cpuper =0.0
    if usni2 - usni1 !=0:
        cpuper=(usn2-usn1)/(usni2-usni1)  
    return cpuper

def strfromfloat(f):
    return str('%.2f' %f)


if __name__=='__main__':
    #get_mem()
    need_to_send_mail =False
    sys_exception_info =''
    sys_info = ''
    d = get_disk()
    m = get_mem()
    print d,m,float(d)>0.8
    if float(d) > 0.8:
        sys_exception_info +='warn:irdev low dist,disk used >80% \n'
        need_to_send_mail = True
    if float(m) > 0.8:
        sys_exception_info+='warn:irdev low mem,mem used >80% \n'
        need_to_send_mail = True
    meminfo = 'disk:'+str(d*100)+'%\n'
    meminfo+='mem:'+str(float(m)*100)+'%\n'
    #print meminfo
    sys_info+=meminfo
    
    muti_core_cpu_info = read_cpu_usage()
    time.sleep(2)
    muti_core_cpu_info2 = read_cpu_usage()
    index=0
    cpu_info ='cpu info:\n'
    for cpustr in muti_core_cpu_info:
        cpustr2 = muti_core_cpu_info2[index]
        #print cpustr,cpustr2
        cpu_percent= calc_cpu_usage(cpustr,cpustr2)
        if index==0:
            cpu_info+='total:'+strfromfloat(cpu_percent*100)+'%,'
            if float(cpu_percent)>0.5:
                sys_exception_info+='warn:hight cpu usge,load more than 50%.\n'
                need_to_send_mail = True
        else:
            cpu_info+='core['+str(index)+']:'+strfromfloat(cpu_percent*100)+'%,'
        index+=1
    #print cpu_info
    sys_info+=cpu_info
    except_mail_info='-----------system warning-----------</br>\n'
    except_mail_info +=sys_exception_info
    except_mail_info+='</br>-----------system status as follws--</br>\n'
    except_mail_info+=sys_info
    print except_mail_info
    #print sys_info
    toUserList = ['root@localhost.com']
    #toUserList = ["root@localhost.com","houjianyu@localhost.com"]
    if need_to_send_mail:
        sendmail('[monitor]sys_warning exception','',toUserList,except_mail_info)

