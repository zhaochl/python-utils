#!/usr/bin/env python
# coding=utf-8
"""
[{k1:v1},{k1:v2}] => 
<th>k1</th>
<tr><td>v1</td></tr>
<tr><td>v2</td></tr>

stat_key 按照某一行进行计数展示
"""
def rendar_request_html(dict_list,stat_key=None):
    caption_info="<caption></caption>"
    result_html = """
    <table class="table table-striped">  
    {0}
    <thead>  
        <tr id="table_head">
    """.format(caption_info)
    rhead = []   
    for d in dict_list:
        for key in d.keys():
            result_html+="<th>"+str(key)+"</th>"
            rhead.append(key)
        break
    result_html+="""
        </tr>  
    </thead> 
        """
    status_count_dict = {}
    for d in dict_list:
        line_str ='<tr>'
        line_str=''
        for key in rhead:
            value = d[key]
            line_str+="<td>"+str(value)+"</td>\n"

            if stat_key!=None and key==stat_key:
                if status_count_dict.has_key(value):
                    status_count_dict[value]+=1
                else:
                    status_count_dict[value]=1

        line_str +='</tr>\n'
        result_html += line_str
    result_html +="""
    </tbody>  
    </table>"""
    
    caption_info_new="<caption>统计:共<span id=show_count>"+str(len(dict_list))+"</span>个"
    if stat_key!=None:
        caption_info_new +='其中:'
        for _status,_count in status_count_dict.iteritems():
            line_str=str(_status)+":<span id=show_count>"+str(_count)+"</span>,"
            caption_info_new+=line_str
    caption_info_new+="</caption>"
    result_html= result_html.replace(caption_info,caption_info_new)

    return result_html

"""
input 
def data_loader():
results,colum = DataUtil.db_query_info('online','mydb',sql)
rhead=['logId','query','creationTime','exactMatchCount','searchtype','clicked']
rdata = list(results)
return rdata,rhead
demo: http://localhost:1114/user_search_log?from_time=2016-07-27&to_time=2016-07-27&platformtype=app,admin&userid=880&name=%E5%BC%A0%E5%BF%83%E5%8A%9B
[{k1:v1},{k1:v2}] => 
<th>k1</th>
<tr><td>v1</td></tr>
<tr><td>v2</td></tr>
stat_key 按照某一行进行计数展示
"""
def rendar_query_result_html(rhead,rdata_list,stat_key=None):
    caption_info="<caption></caption>"
    result_html = """
    <table class="table table-striped">  
    {0}
    <thead>  
        <tr id="table_head">
    """.format(caption_info)
    for key in rhead:
        result_html+="<th>"+str(key)+"</th>"
    result_html+="""
        </tr>  
    </thead> 
        """
    status_count_dict = {}
    line_str=''
    for rdata in rdata_list:
        line_str ='<tr>'
        for index,key in enumerate(rdata):
            value = str(rdata[index]).encode('utf8')

            if key=='query':
                query = value
                query_link ="<a href='http://localhost/search?query="+quote(query)+"' target='_blank'>"+query+"</a>"
                line_str+="<td>"+query_link+"</td>\n"
                print query_link,line_str
            else:
                line_str+="<td>"+str(value)+"</td>\n"

            if stat_key!=None and key==stat_key:
                if status_count_dict.has_key(value):
                    status_count_dict[value]+=1
                else:
                    status_count_dict[value]=1

        line_str +='</tr>\n'
        result_html += line_str
    result_html +="""
    </tbody>  
    </table>"""
    
    caption_info_new="<caption>统计:共<span id=show_count>"+str(len(rdata_list))+"</span>个"
    if stat_key!=None:
        caption_info_new +='其中:'
        for _status,_count in status_count_dict.iteritems():
            line_str=str(_status)+":<span id=show_count>"+str(_count)+"</span>,"
            caption_info_new+=line_str
    caption_info_new+="</caption>"
    result_html= result_html.replace(caption_info,caption_info_new)

    return result_html



"""
by zcl at 2016.6.15
"""
def rendar_mail_table(title,notice,rhead_list,rdata_list):
    
    html ="""
    <p class="section">{0}</p>
    <p class="section">{1}</p>
    <table cellpadding="5" cellspacing="0" border="1" bordercolor="#04B4AE" style="text-align: center; font-family: Arial; border-collapse: collapse; width: auto;">
    <tbody>
        <tr>
            <td colspan="{2}"><div>{0}</div></td>
        </tr>
        <tr>
    """.format(title,notice,str(len(rhead_list)))
    for rhead in rhead_list:
        rhead = rhead.encode('utf8')
        tmp = """<th style="background-color: #04B4AE; color: #ffffff">{0}</th>
        """.format(str(rhead))
        html+=tmp
    html+="</tr>"

    for o in rdata_list:
        line_html=''
        line_html+="<tr>"
        for key in rhead_list:
            val = o[key]
            key = key.encode('utf8')
            line_html+="<td>"+str(val)+"</td>"
        line_html+="</tr>"
        html+=line_html
    html+="""
        </tbody>
        </table>
        <hr>
        """
    return html



if __name__=='__main__':
    #rdata=[{'a':1,'b':'2','status':1},{'a':-1,'b':'-2','status':0},{'a':3,'b':3,'status':1}]
    #html = rendar_html(a,'status')
    rdata=[[1,1,1],[2,2,2],[3,3,3]]
    rhead = ['a','b','status']
    html = rendar_query_result_html(rhead,rdata)
    print html
