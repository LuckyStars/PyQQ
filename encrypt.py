#coding:utf-8
import hashlib

def md5(strvalue):
    #return hashlib.md5(strvalue.encode("ISO-8859-1") ).hexdigest()
    return hashlib.md5(strvalue).hexdigest()

def hexchar2bin(strvalue):
    temp = ''
    for i in range(0, len(strvalue), 2):
        temp += chr(int(strvalue[i:i+2],16))
    return temp

def uin2hex(strvalue):
    maxLength = 16
    tempstr = int(strvalue, 10)
    hexstrvalue = hex(tempstr).replace('0x','')
    hexlength = len(hexstrvalue)
    for i in range(maxLength - hexlength):
        hexstrvalue = "0" + hexstrvalue
    result = ''
    for j in range(0, maxLength, 2):
        result += hexstrvalue[j:j+2]
    return result

def encrypt(password, uin, verifycode):
    # 结果=MD5(MD5(hexchar2bin(MD5(密码))+pt.uin)+大写验证码)
    # pt.uin，我们将\x00\x00\x00\x00\x3c\xcb\x48\x45分为00 00 00 00 3c cb 48 45
    # 然后对每组16进制数字转换成ASCII字符，然后连接起来就是pt.uin
    uin = hexchar2bin(uin2hex(uin))  
    I = password
    F = hexchar2bin(md5(I))
    E = md5(F+uin).upper()
    D = md5(E+verifycode.upper()).upper()
    return D

def getHash1(a,e):
    c = []
    for i in a:
        c.append(int(i))
    b = 0
    k = -1
    for i in c:
        b += i
        b %= len(e)
        f = 0
        if (b + 4 > len(e)):
            h = 0
            g = 4 + b - len(e)
            while  h < 4:
                if h < g:
                    f |= (ord(e[b + h]) & 255) << (3 - h) * 8
                else:
                    f |= (ord(e[h - g]) & 255) << (3 - h) * 8
                h += 1
        else:
            h = 0
            while h < 4:
                f |= (ord(e[b + h]) & 255) << (3 - h) * 8
                h += 1
#        print i,f
        k ^= f
    c = [k >> 24 & 255,k >> 16 & 255,k >> 8 & 255,k & 255]
    k = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    d = ""
    b = 0
    while b < len(c):
        d += k[c[b] >> 4 & 15]
        d += k[c[b] & 15]
        b += 1
    return d

#加密文件地址http://0.web.qstatic.com/webqqpic/pubapps/0/50/eqq.all.js，搜索function(b,i
def getHash2(qq, ptwebqq):
    a = ptwebqq + 'password error'
    s = ''
    j = []
    while True:
        if (len(s) <= len(a)):
            s += qq
            if (len(s) == len(a)):
                break 
        else:
            s = s[0:len(a)]
            break
    for d in xrange(len(s)):
        j.append(ord(s[d]) ^ ord(a[d]))
    a = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    s = ""
    for d in xrange(len(j)):
        s += a[j[d] >> 4 & 15]
        s += a[j[d] & 15]
    return s

def getHash3(b,i):
    a=[]  
    s=0  
    for s in range(0,len(b)):  
        t=int(b[s])  
        a.append(t)   
    j = 0  
    d = -1  
    s = 0  
    for s in range(0,len(a)):  
        j = j + a[s]  
        j = j % len(i)  
        c = 0  
        if (j + 4) > len(i):   
            l = 4 + j - len(i)  
            for x in range(0,4):  
                if x < l:  
                    c = c | (( ord(i[j + x]) & 255) << (3 - x) * 8 )  
                else:  
                    c = c | ( ( ord(i[x - l]) & 255) << (3 - x) * 8 )  
        else:  
            for x in range(0,4):  
                c = c | (( ord(i[j + x]) & 255) << (3 - x) * 8 )  
        d = d ^ c     
          
    a = [0,0,0,0]  
    a[0] = d >> 24 & 255  
    a[1] = d >> 16 & 255  
    a[2] = d >> 8 & 255  
    a[3] = d & 255  
    d = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]  
    s = ""  
    for j in range(0,len(a)):  
        s = s + d[a[j] >> 4 & 15]  
        s = s + d[a[j] & 15]  
    return s 

def get_hash(qq, ptwebqq):
    return getHash3(qq, ptwebqq)

password = 'wr6740495'
uin = '1213247447'
verifycode = '!IAC'

#F8F6ACAC
vfwebqq = '9a8d442b02dbde99248a85eb59aababc5f48785c48b74ca70be3962d3a5537ebdc330f66595221a2'

#print get_hash(uin, vfwebqq)
#print get_hash('195','5b5cecfea030bc7f06aad2ca6f650d059334a3d152fba9926bd82717188c3b66')
#{"h":"hello","hash":"F7F8A4FD","vfwebqq":"7e42206c73c8c4b526408e749537ec437eee9f39a89441d97573038296159ea24ad171a17ff102b9"}
ptwebqq = '7c07d3ddf87573ac01067b2e36ff0e8633aca9c64af1a99f3d789b30e9e546f7'
#print getHash2(uin, ptwebqq)
#print getHash3(uin, ptwebqq)
#print get_hash(uin, '7e42206c73c8c4b526408e749537ec437eee9f39a89441d97573038296159ea24ad171a17ff102b9')

# print uin2hex(uin)
# print hexchar2bin(uin2hex(uin))
# print hexchar2bin(md5(password))
# uin = hexchar2bin(uin2hex(uin))  
# I = password
# F = hexchar2bin(md5(I))
# E = md5(F+uin).upper()
# D = md5(E+verifycode.upper()).upper()
# print md5(F+uin)
# print D
# print encrypt(password, uin, verifycode)
