#!/usr/bin/python
# -*- coding: UTF-8 -*-

import random
import time

#生成指定二进制位数的奇数
def proBin(w):  # w表示希望产生位数
    list = []
    list.append('1')  #最高位定为1
    for i in range(w - 2):
        c = random.choice(['0', '1'])
        list.append(c)
    list.append('1') # 奇数
    res = int(''.join(list),2)
    return res,list

#a^d mod n
#蒙哥马利算法
def montgomery(a, d, n):
    x = 1
    while d:
        if (d & 1):
            x = (x * a) % n
        d >>= 1
        a = (a * a) % n
    return x

#MillerRabin算法素性检验
def MillerRabin(res,list,len):
    N = list[:]
    s=0
    d=0

    # N-1 = d*2^s,求d, s
    N[-1] = '0'
    for i in range(len):
        if(N[-(i+1)] == '0'):
            s += 1
        else:
            d = list[0:-i]
            break

    d=int(''.join(d),2)
    #检测test次
    test = 10
    flag = 0
    for i in range(test):
        a = random.randint(1,res-1)
        x = montgomery(a, d, res)
        if(x != 1):
            #是否存在r使得a^(d*2^r) mod N = -1
            for r in range(s):
                m =2**r*d
                y = montgomery(a, m, res)
                if(y == res-1):
                    flag = 1
                    break
            if(flag == 0):
                return 0
    return 1

#生成指定位数素数
def prime(len):
    re = 0
    while(re == 0):
        res, list = proBin(len)
        re = MillerRabin(res, list, len)
    return res,list

#--------------------------------------------------------------------------------------------------------------------
#求模逆...
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

# 定义一个函数，参数分别为a,n，返回值为b
def findModReverse(a, m):  # 扩展欧几里得算法求模逆

    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % m



#--------------------------------------------------------------------------------------------------------------------

# M位明文，(e,n)为公钥对，使用公钥对明文进行加密
def encode(M,e,n,z):
    inl = z-1    #分组位数
    m = str(M)
    length = len(m)
    c = ''
    #将m分组进行加密
    for i in range(int(length/inl)):
        n_t = m[inl*i:inl*(i+1)]    #取位
        n_t = int(n_t)
        c_t = montgomery(n_t,e,n)
        c += str(c_t)
    n_t = m[int(length/inl)*inl:length]    #剩余位
    n_t = int(n_t)
    c_t = montgomery(n_t, e, n)
    c += str(c_t)
    c = int(c)
    return c

def decode(C,d,n,z):
    inl = z
    c = str(C)
    length = len(c)
    m = ''
    # 将c分组进行解密
    for i in range(int(length / inl)):
        n_t = c[inl * i:inl * (i + 1)]
        n_t = int(n_t)
        m_t = montgomery(n_t, d, n)
        m += str(m_t)
    n_t = c[int(length/inl) * inl:length]  # 剩余位
    n_t = int(n_t)
    m_t = montgomery(n_t, d, n)
    m += str(m_t)
    m = int(m)
    return m

if __name__ == '__main__':

    #生成512位素数p,q用于公钥私钥
    LEN=512
    p,list_p=prime(LEN)
    q,list_q=prime(LEN)

    #(n,e)--公钥对
    e = 65537    #2^16+1
    n = p*q
    #(n,d)--私钥对
    phi = (p-1)*(q-1)
    d=findModReverse(e,phi)    #ed mod phi = 1
    #加密_test
    M=1356205320457610288745198967657644166379972189839804389074591563666634066646564410685955217825048626066190866536592405966964024022236587593447122392540038493893121248948780525117822889230574978651418075403357439692743398250207060920929117606033490559159560987768768324823011579283223392964454439904542675637683985296529882973798752471233683249209762843835985174607047556306705224118165162905676610067022517682197138138621344578050034245933990790845007906416093198845798901781830868021761765904777531676765131379495584915533823288125255520904108500256867069512326595285549579378834222350197662163243932424184772115345
    z = len(str(n))
    C = encode(M, e, n, z)

    #解密
    M0 = decode(C, d, n, z)

    print('生成素数对：\n',p,'\n',q)
    print('------------------------------------------------------------------------')
    print('明文：\n',M)
    print('密文：\n',C)
    print('密文解密结果：\n',M0)

