# !/usr/bin/python3
# -*- coding:utf-8 -*-

import ctypes

dword_6661C0 = []
byte_6651C0 = []
with open("tables/6661C0.txt", "r")as F:
    dword_6661C0 = eval(F.read().strip())
    F.close()

with open("tables/6651C0.txt", "r")as F:
    byte_6651C0 = eval(F.read().strip())
    F.close()

byte_6650C0 = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,1,0,3,2,5,4,7,6,9,8,11,10,13,12,15,14,2,3,0,1,6,7,4,5,10,11,8,9,14,15,12,13,3,2,1,0,7,6,5,4,11,10,9,8,15,14,13,12,4,5,6,7,0,1,2,3,12,13,14,15,8,9,10,11,5,4,7,6,1,0,3,2,13,12,15,14,9,8,11,10,6,7,4,5,2,3,0,1,14,15,12,13,10,11,8,9,7,6,5,4,3,2,1,0,15,14,13,12,11,10,9,8,8,9,10,11,12,13,14,15,0,1,2,3,4,5,6,7,9,8,11,10,13,12,15,14,1,0,3,2,5,4,7,6,10,11,8,9,14,15,12,13,2,3,0,1,6,7,4,5,11,10,9,8,15,14,13,12,3,2,1,0,7,6,5,4,12,13,14,15,8,9,10,11,4,5,6,7,0,1,2,3,13,12,15,14,9,8,11,10,5,4,7,6,1,0,3,2,14,15,12,13,10,11,8,9,6,7,4,5,2,3,0,1,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]

for i in range(len(dword_6661C0)):
    dword_6661C0[i]=ctypes.c_uint32(dword_6661C0[i]).value

for i in range(len(byte_6651C0)):
    byte_6651C0[i]=ctypes.c_uint8(byte_6651C0[i]).value

def swap(s):
    res = [i for i in range(16)]
    res[0] = s[0]
    res[1] = s[5]
    res[2] = s[10]
    res[3] = s[15]
    res[4] = s[4]
    res[5] = s[9]
    res[6] = s[0xe]
    res[7] = s[3]
    res[8] = s[8]
    res[9] = s[0xd]
    res[10] = s[2]
    res[11] = s[7]
    res[12] = s[0xc]
    res[13] = s[1]
    res[14] = s[6]
    res[15] = s[0xb]
    return "".join(res)

def xor(a,b):
    return "".join(chr(ord(a[i])^ord(b[i])) for i in range(16))

def encrypt(inp):
    for v8 in range(9):
        res = [i for i in range(16)]
        inp = swap(inp)
        for v9 in range(4):
            v3 = dword_6661C0[((4 * v9 + 16 * v8) << 8) + ord(inp[4*v9])]
            v4 = dword_6661C0[((4 * v9 + 1 + 16 * v8) << 8) + ord(inp[4*v9+1])]
            v5 = dword_6661C0[((4 * v9 + 2 + 16 * v8) << 8) + ord(inp[4*v9+2])]
            v6 = dword_6661C0[((4 * v9 + 3 + 16 * v8) << 8) + ord(inp[4*v9+3])]
            res[4*v9] = chr(byte_6650C0[(16*byte_6650C0[16*(v3 & 0xF)+(v4&0xf)]+byte_6650C0[16*(v5 & 0xF)+(v6&0xf)])]  | byte_6650C0[16*byte_6650C0[16*((v3>>4)&0xf)+((v4>>4)&0xf)]+byte_6650C0[16*((v5>>4)&0xf)+((v6>>4)&0xf)]]*16)
            v3 = v3 >> 8
            v4 = v4 >> 8
            v5 = v5 >> 8
            v6 = v6 >> 8
            res[4*v9+1] = chr(byte_6650C0[(16*byte_6650C0[16*(v3 & 0xF)+(v4&0xf)]+byte_6650C0[16*(v5 & 0xF)+(v6&0xf)])] | byte_6650C0[16*byte_6650C0[16*((v3>>4)&0xf)+((v4>>4)&0xf)]+byte_6650C0[16*((v5>>4)&0xf)+((v6>>4)&0xf)]]*16)
            v3 = v3 >> 8
            v4 = v4 >> 8
            v5 = v5 >> 8
            v6 = v6 >> 8
            res[4*v9+2] = chr(byte_6650C0[(16*byte_6650C0[16*(v3 & 0xF)+(v4&0xf)]+byte_6650C0[16*(v5 & 0xF)+(v6&0xf)])] | byte_6650C0[16*byte_6650C0[16*((v3>>4)&0xf)+((v4>>4)&0xf)]+byte_6650C0[16*((v5>>4)&0xf)+((v6>>4)&0xf)]]*16)
            v3 = v3 >> 8
            v4 = v4 >> 8
            v5 = v5 >> 8
            v6 = v6 >> 8
            res[4*v9+3] = chr(byte_6650C0[(16*byte_6650C0[16*(v3 & 0xF)+(v4&0xf)]+byte_6650C0[16*(v5 & 0xF)+(v6&0xf)])] | byte_6650C0[16*byte_6650C0[16*((v3>>4)&0xf)+((v4>>4)&0xf)]+byte_6650C0[16*((v5>>4)&0xf)+((v6>>4)&0xf)]]*16)
        inp = "".join(res)

    inp = swap(inp)
    res = [i for i in range(16)]

    for i in range(16):
        res[i] = "{:02x}".format(byte_6651C0[256*i + ord(inp[i])])
    inp = "".join(res)
    return inp

print(encrypt("0123456789abcdef"))