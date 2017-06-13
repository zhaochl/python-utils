#!/usr/bin/env python
# coding=utf-8

import os
import M2Crypto
def test2():
    import rsa
 
    # 先生成一对密钥，然后保存.pem格式文件，当然也可以直接使用
    (pubkey, privkey) = rsa.newkeys(1024)
     
    pub = pubkey.save_pkcs1()
    pubfile = open('public.pem','w+')
    pubfile.write(pub)
    pubfile.close()
     
    pri = privkey.save_pkcs1()
    prifile = open('private.pem','w+')
    prifile.write(pri)
    prifile.close()
     
    # load公钥和密钥
    message = 'lovesoo.org'
    with open('public.pem') as publickfile:
        p = publickfile.read()
        pubkey = rsa.PublicKey.load_pkcs1(p)
     
    with open('private.pem') as privatefile:
        p = privatefile.read()
        privkey = rsa.PrivateKey.load_pkcs1(p)
     
    # 用公钥加密、再用私钥解密
    crypto = rsa.encrypt(message, pubkey)
    message = rsa.decrypt(crypto, privkey)
    print message
     
    # sign 用私钥签名认证、再用公钥验证签名
    signature = rsa.sign(message, privkey, 'SHA-1')
    rsa.verify('lovesoo.org', signature, pubkey)

def test1():
    #随机数生成器(1024位随机)
    M2Crypto.Rand.rand_seed(os.urandom(1024))
    #生成一个1024位公钥与私密钥证书
    Geekso = M2Crypto.RSA.gen_key(1024, 65537)
    Geekso.save_key('jb51.net-private.pem', None)
    Geekso.save_pub_key('jb51.net-public.pem')
    #使用公钥证书加密开始
    WriteRSA = M2Crypto.RSA.load_pub_key('jb51.net-public.pem')
    CipherText = WriteRSA.public_encrypt("这是一个秘密消息,只能用私钥进行解密",M2Crypto.RSA.pkcs1_oaep_padding)
    print "加密的串是:"
    print CipherText.encode('base64')
    #对加密串进行签名
    MsgDigest = M2Crypto.EVP.MessageDigest('sha1')
    MsgDigest.update(CipherText)
    #提示，这里也可以使用私钥签名
    #WriteRSA = M2Crypto.RSA.load_key ('jb51.net-private.pem')
    #Signature = WriteRSA.sign_rsassa_pss(MsgDigest.digest())
    Signature = Geekso.sign_rsassa_pss(MsgDigest.digest())
    print "签名的串是:"
    print Signature.encode('base64')
    #使用私钥证书解密开始
    ReadRSA = M2Crypto.RSA.load_key ('jb51.net-private.pem')
    try:
        PlainText = ReadRSA.private_decrypt (CipherText, M2Crypto.RSA.pkcs1_oaep_padding)
    except:
        print "解密错误"
        PlainText = ""
    if PlainText :
       print "解密出来的串是:"
       print PlainText
       # 验证加密串的签名
       MsgDigest = M2Crypto.EVP.MessageDigest('sha1')
       MsgDigest.update(CipherText)
       #提示，如果是用私钥签名的那就用公钥验证
       #VerifyRSA = M2Crypto.RSA.load_pub_key('Alice-public.pem')
       #VerifyRSA.verify_rsassa_pss(MsgDigest.digest(), Signature)
       if Geekso.verify_rsassa_pss(MsgDigest.digest(), Signature) == 1:
           print "签名正确"
       else:
           print "签名不正确"
def test3():
    from Crypto import Random
    from Crypto.Hash import SHA
    from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
    from Crypto.Signature import PKCS1_v1_5 as Signature_pkcs1_v1_5
    from Crypto.PublicKey import RSA

    # 伪随机数生成器
    random_generator = Random.new().read
    # rsa算法生成实例
    rsa = RSA.generate(1024, random_generator)

    # master的秘钥对的生成
    private_pem = rsa.exportKey()

    with open('master-private.pem', 'w') as f:
        f.write(private_pem)

    public_pem = rsa.publickey().exportKey()
    with open('master-public.pem', 'w') as f:
        f.write(public_pem)

    # ghost的秘钥对的生成
    private_pem = rsa.exportKey()
    with open('master-private.pem', 'w') as f:
        f.write(private_pem)

    public_pem = rsa.publickey().exportKey()
    with open('master-public.pem', 'w') as f:
        f.write(public_pem)               

if __name__=='__main__':
    #test1()
    #test2()
    test3()
