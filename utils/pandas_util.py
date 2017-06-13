#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import numpy as np
from  pdb import *


df = pd.DataFrame({
    'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
    'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
    'sex': ['Female', 'Male', 'Male', 'Male', 'Female']
})

print df
# data type of columns
print df.dtypes
# indexes
print df.index
# return pandas.Index
#print df.columns
# each row, return array[array]
#print df.values
"""
select total_bill,tip from df where id>=1 and id<=3
"""
df_sub = df.loc[1:3, ['total_bill', 'tip']]
print df_sub
"""
{'tip': {1: 1.6599999999999999, 2: 3.5, 3: 3.3100000000000001}, 'total_bill': {1: 10.34, 2: 23.68, 3: 23.68}}
"""
print df_sub.to_dict()

df_sub = df.loc[0:, ['total_bill']]
print df_sub.to_dict()

print df.iloc[1:3, 1: 3]
#print df.at[3, 'tip']

print df[1:3],df[1:3].to_dict()

print df['tip'],df['tip'].to_dict()


"""
query where
"""
print df[df['sex'] == 'Female']
print df[df['total_bill'] > 20]

# or
print df.query('total_bill > 20')

# and
print df[(df['sex'] == 'Female') & (df['total_bill'] > 20)]
# or
print df[(df['sex'] == 'Female') | (df['total_bill'] > 20)]
# in
print df[df['total_bill'].isin([21.01, 23.68, 24.59])]
# not
print df[-(df['sex'] == 'Male')]

# string function
#print df[(-df.app.str.contains('^微信\d+$'))]

"""
get one value
"""
total = df.loc[df['tip'] == 1.66, 'total_bill'].values[0]
print total

"""
distinct
drop_duplicates根据某列对dataframe进行去重
"""
print df.drop_duplicates(['sex'], keep='last')

print '***'*10,'group'
"""
group
group一般会配合合计函数（Aggregate functions）使用，比如：count、avg等。Pandas对合计函数的支持有限，有count和size函数实现SQL的count：
"""
print df.groupby('sex').size()
print df.groupby('sex').count()
print df.groupby('sex')['tip'].count()

"""
select sex, max(tip), sum(total_bill) as total
from tips_tb
group by sex;
"""
print df.groupby('sex').agg({'tip': np.max, 'total_bill': np.sum})

# count(distinct **)
print df.groupby('tip').agg({'sex': pd.Series.nunique})

# first implementation
df.columns = ['total', 'pit', 'xes']
print df

# second implementation
print df.rename(columns={'total_bill': 'total', 'tip': 'pit', 'sex': 'xes'}, inplace=True)

"""
join
Pandas中join的实现也有两种：
第一种方法是按DataFrame的index进行join的，而第二种方法才是按on指定的列做join。Pandas满足left、right、inner、full outer四种join方式。
"""
# 1.
#df.join(df2, how=‘left‘...)

# 2. 
#pd.merge(df1, df2, how=‘left‘, left_on=‘app‘, right_on=‘app‘)

"""
as
SQL中使用as修改列的别名，Pandas也支持这种修改：
"""
"""
order
Pandas中支持多列order，并可以调整不同列的升序/降序，有更高的排序自由度：
"""
#print df.sort_values(['total_bill', 'tip'], ascending=[False, True])
print df.sort_values(['total', 'pit'], ascending=[False, True])


import pandas as pd
a=[[1,2,3],[4,5,6]]
b=pd.DataFrame(a)
c=b[0]*b[1]
#df.insert(idx, col_name, value)
#insert 三个参数，插到第几列，该列列名，值
b.insert(3,3,c)

print b

d1= pd.DataFrame()
data = {'a':1,'b':2}
d1 = d1.from_dict(data,orient='index')
print d1
set_trace()
print d1.to_dict(orient='dict')

#[{'a': 1, 'b': 2}]
print d1.T.to_dict(orient='records')
