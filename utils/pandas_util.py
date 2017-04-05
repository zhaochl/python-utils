#!/usr/bin/env python
# coding=utf-8
import pandas as pd
import numpy as np





#df1 = pd.DataFrame({'key': ['a', 'b', 'b'], 'data1': range(3)})

#df2 = pd.DataFrame({'key': ['a', 'b', 'c'], 'data2': range(3)})

#df3 = pd.merge(df1, df2)  # 没有指定连接键，默认用重叠列名，没有指定连接方式

#print df3
"""
Series是一种类似于一位数组的对象，它由一组数据（各种NumPy数据类型）以及与之相关的数据标签组成
Series的表现形式为：索引在左边，值在右边。由于我们没有为它指定索引，于是会自动的创建一个0~N-1的整数值索引。我们可以分开看索引与值
"""

obj = pd.Series([1,5,7,8,78])
print obj
print obj.index
print obj.values
print pd.RangeIndex(start=0, stop=5, step=1)
#[ 1  5  7  8 78 ]
#
"""
我们也可以自己指定索引
print 
Index([u'one', u'two', u'three', u'four', u'five'], dtype='object')
[ 1  5  7  8 78 ]
"""
obj = pd.Series([1,5,7,8,78],index=['one','two','three','four','five'])
print obj.index
print obj.values

"""
我们发现这个时候obj的索引值变为我们制定的值 
我们可以通过索引值取得我们想要的值
"""
print obj['one']
print obj[['one','three','five']]
print obj[obj>=7]

va={"one":"a","two":"b","three":"c","four":"d"}
obj = pd.Series(va,index=['one','two','three','four','five'])
print obj

print obj.isnull()

data={'index':[1,2,3,4,5],'year':[2012,2013,2014,2015,2016],'status':['good','very good','well','very well','wonderful']}
frame = pd.DataFrame(data)
print frame
data2={"kk":np.array([5,6,7,8,9]),"jj":np.array([15,16,17,18,19])}
frame = pd.DataFrame(data2)
print frame

frame2 = pd.DataFrame(data,columns=['status','year','index'],index=['one','two','three','four','five'])
print frame2

print frame2.to_html(header=header)



#d = {1:"a",2:"b",3:"c"}
d = {
    1:{"a":11,"b":12,"c":13},
    2:{"a":21,"b":22,"c":23},
    3:{"a":31,"b":32,"c":33}
}
pd = pd.DataFrame.from_dict(d,orient='index')
csv_file = '/tmp/t'
pd.to_csv(csv_file)
print pd
