#!/usr/bin/env python
# coding=utf-8

import pandas as pd
import numpy as np
from  pdb import *

def test():
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
    #set_trace()
    #print d1.to_dict(orient='dict')

    #[{'a': 1, 'b': 2}]
    print d1.T.to_dict(orient='records')
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

    #print frame2.to_html(header=header)



d = {
    1:{"a":11,"b":12,"c":13},
    2:{"a":21,"b":22,"c":23},
    3:{"a":31,"b":32,"c":33}
}
d = {1:"a",2:"b",3:"c"}
df2 = pd.DataFrame.from_dict(d,orient='index')
print df2

df = pd.DataFrame({
        'total_bill': [16.99, 10.34, 23.68, 23.68, 24.59],
        'tip': [1.01, 1.66, 3.50, 3.31, 3.61],
        'sex': ['Female', 'Male', 'Male', 'Male', 'Female']
    })
print df
def test_csv():
    #csv_file = '/tmp/t'
    #pd.to_csv(csv_file)
    #print pd
    csv_obj = df.to_csv(sep='|',index=False,header=False)
    print csv_obj


def test_apply():
    df2 = pd.T
    print df2
    def add(x):
        return x+'x'
    df2[1] =df2[1].apply(add)
    print df2
if __name__=='__main__':
    test_csv()
