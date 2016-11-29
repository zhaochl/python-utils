#!/bin/bash

#http://blog.csdn.net/yczz/article/details/5974235

> show dbs;
local       0.000GB
monitoring  0.001GB
> use monitoring;
switched to db monitoring
> db.alerts.findOne();
{
    "_id" : "40511de2-696e-48f1-a14f-eca77a8634a4",
    "origin" : "main_extract.py/irdev",

1.  超级用户相关：
         1. #进入数据库admin
use admin
         2. #增加或修改用户密码
          db.addUser('name','pwd')
         3. #查看用户列表
          db.system.users.find()
         4. #用户认证
          db.auth('name','pwd')
         5. #删除用户
          db.removeUser('name')
         6. #查看所有用户
          show users
         7. #查看所有数据库
          show dbs
         8. #查看所有的collection
          show collections
         9. #查看各collection的状态
          db.printCollectionStats()
        10. #查看主从复制状态
          db.printReplicationInfo()
        11. #修复数据库
          db.repairDatabase()
        12. #设置记录profiling，0=off 1=slow 2=all
          db.setProfilingLevel(1)
        13. #查看profiling
          show profile
        14. #拷贝数据库
          db.copyDatabase('mail_addr','mail_addr_tmp')
        15. #删除collection
          db.mail_addr.drop()
        16. #删除当前的数据库
          db.dropDatabase()
       
   2. 增删改
         1. #存储嵌套的对象
db.foo.save({'name':'ysz','address':{'city':'beijing','post':100096},'phone':[138,139]})
 
         2. #存储数组对象
db.user_addr.save({'Uid':'yushunzhi@sohu.com','Al':['test-1@sohu.com','test-2@sohu.com']})
 
         3. #根据query条件修改，如果不存在则插入，允许修改多条记录
            db.foo.update({'yy':5},{'$set':{'xx':2}},upsert=true,multi=true)
         4. #删除yy=5的记录
            db.foo.remove({'yy':5})
         5. #删除所有的记录
            db.foo.remove()
 
   3. 索引
         1. #增加索引：1(ascending),-1(descending)
         2. db.foo.ensureIndex({firstname: 1, lastname: 1}, {unique: true});
         3. #索引子对象
         4. db.user_addr.ensureIndex({'Al.Em': 1})
         5. #查看索引信息
         6. db.foo.getIndexes()
         7. db.foo.getIndexKeys()
         8. #根据索引名删除索引
         9. db.user_addr.dropIndex('Al.Em_1')
 
   4. 查询
         1. #查找所有
        2. db.foo.find()
        3. #查找一条记录
        4. db.foo.findOne()
        5. #根据条件检索10条记录
        6. db.foo.find({'msg':'Hello 1'}).limit(10)
        7. #sort排序
        8. db.deliver_status.find({'From':'ixigua@sina.com'}).sort({'Dt',-1})
         9. db.deliver_status.find().sort({'Ct':-1}).limit(1)
        10. #count操作
        11. db.user_addr.count()
        12. #distinct操作,查询指定列，去重复
        13. db.foo.distinct('msg')
        14. #”>=”操作
        15. db.foo.find({"timestamp": {"$gte" : 2}})
        16. #子对象的查找
        17. db.foo.find({'address.city':'beijing'})
   5. 管理
         1. #查看collection数据的大小
         2. db.deliver_status.dataSize()
         3. #查看colleciont状态
         4. db.deliver_status.stats()
         5. #查询所有索引的大小
         6. db.deliver_status.totalIndexSize()
