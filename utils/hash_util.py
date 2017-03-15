#!/usr/bin/env python
# coding=utf-8
import os
import hashlib
def test():
    m = hashlib.md5()   #创建hash对象，md5:(message-Digest Algorithm 5)消息摘要算法,得出一个128位的密文
    print m             #<md5 HASH object @ 000000000254ADF0>
    m.update('BeginMan')#更新哈希对象以字符串参数
    print m.digest()    #返回摘要，作为二进制数据字符串值
    print m.hexdigest() #返回十六进制数字字符串    0b28251e684dfbd9102f8b6f0281c0c5
    print m.digest_size #16
    print m.block_size  #64
    url="http://www.cnblogs.com/BeginMan/p/3328172.html"
    md5 = hashlib.md5(str(url)).hexdigest()
    print md5,len(md5)
    h = hash(url)
    print h,len(str(h))
    url2="http://www.cnblogs.com/BeginMan/p/3328171.html"
    h2 = hash(url2)
    print h2
    
    a=hash('a')
    print a,len(str(a))
    ab=hash('ab')
    print ab,len(str(ab))
def hmac_key_encrypt():
    import hmac
    h = hmac.new('python'.encode('utf-8'))
    h.update('helloworld'.encode('utf-8'))
    return (h.hexdigest())

def sha1_key_encrypt():
    hash = hashlib.sha1()
    hash.update('admin'.encode('utf-8'))
    return(hash.hexdigest())

def md5_encrypt():
    ######  md5 加密 ############
    hash = hashlib.md5('python'.encode('utf-8'))
    return(hash.hexdigest())

def md5_salt_encrypt():
    ######  md5 加密 ############
    hash = hashlib.md5('python'.encode('utf-8'))
    hash.update('admin'.encode('utf-8'))
    return (hash.hexdigest())
def sha512_key_encrypt():
    hash = hashlib.sha512()
    hash.update('admin'.encode('utf-8'))
    return (hash.hexdigest())

def sha384_key_encrypt():
    hash = hashlib.sha384()
    hash.update('admin'.encode('utf-8'))
    return (hash.hexdigest())
 
def sha256_key_encrypt():
    hash = hashlib.sha256()
    hash.update('admin'.encode('utf-8'))
    return (hash.hexdigest())  
 
import hashlib
def md5sum(filename):
    """
    用于获取文件的md5值
    :param filename: 文件名
    :return: MD5码
    """
    if not os.path.isfile(filename):  # 如果校验md5的文件不是文件，返回空
        return 'is not file'
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)   
    f.close()
    return myhash.hexdigest()
    

if __name__=='__main__':
    #test()
    #b3b867248bb4cace835b59562c39fd55
    print hmac_key_encrypt()
    #75b431c498b55557591f834af7856b9f
    print md5_encrypt()
    print md5_salt_encrypt()
    print md5sum('hash_util.py')
    print sha1_key_encrypt()
    print sha384_key_encrypt()
    print sha256_key_encrypt()
