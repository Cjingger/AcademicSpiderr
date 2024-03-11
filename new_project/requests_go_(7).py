#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/9/26 17:37
# @Author  : LIU
# @Site    :
# @File    : tes.py
# @Software: PyCharm
import copy
# #Desc:
import re
import string
import hashlib
import random
import time
import zlib
import math
import json

import requests
import vthread
from loguru import logger

api = "http://localhost:6666/fetch"

def http_pramas(data=None):
    result = ""
    for i in data.keys():
        result += f"{i}={data.get(i)}&"
    return result[:-3]
def http_form_data(data=None):
    result = ""
    for i in data.keys():
        result += f"{i}={data.get(i)}|||"
    return result[:-3]

def random_str(length, slat=string.hexdigits):
    _str = ""
    for _ in range(length):
        _str += random.choice(slat)
    return _str

def get_proxies(tll=30):
    _str = random_str(6, string.ascii_lowercase + string.digits)
    username = f"test__test-zone-static-region-us-session-session-300{_str}-sessTime-{tll}"
    password = "qweasdzxc1"
    address = "proxy.ipidea.io:2336"

    return {
        "address": address,
        "username": username,
        "password": password
    }

    # return {
    #     "http": f"http://fadsff5-zone-resi:fadsff5@pr-na.pyproxy.com:16666",
    #     "https": f"http://fadsff5-zone-resi:fadsff5@pr-na.pyproxy.com:16666",
    # }

    # return {
    #     "http": f"http://{username}:{password}@{address}/",
    #     "https": f"http://{username}:{password}@{address}/",
    # }




class BeeEncode(object):
    def __init__(self):
        self._dict = {
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="117", "Google Chrome";v="117"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="116", "Google Chrome";v="116"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="115", "Google Chrome";v="115"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="113", "Google Chrome";v="113"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="112", "Google Chrome";v="112"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="111", "Google Chrome";v="111"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="110", "Google Chrome";v="110"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="109", "Google Chrome";v="109"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="107", "Google Chrome";v="107"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="106", "Google Chrome";v="106"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="105", "Google Chrome";v="105"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="104", "Google Chrome";v="104"',
            # 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="103", "Google Chrome";v="103"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="117", "Google Chrome";v="117"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="116", "Google Chrome";v="116"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="115", "Google Chrome";v="115"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="113", "Google Chrome";v="113"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="112", "Google Chrome";v="112"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="111", "Google Chrome";v="111"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36': '"Not?A_Brand";v="24", "Chromium";v="110", "Google Chrome";v="110"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="109", "Google Chrome";v="109"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="107", "Google Chrome";v="107"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="106", "Google Chrome";v="106"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36': '"Not?A_Brand";v="8", "Chromium";v="105", "Google Chrome";v="105"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="104", "Google Chrome";v="104"',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36': '"Not?A_Brand";v="99", "Chromium";v="103", "Google Chrome";v="103"'
        }

    def _easy_json_to_http_form_data(self, data=None):
        result = ""
        for i in data.keys():
            result += f"{i}={data.get(i)}&"
        return result[:-1]

    def get_FKGJ(self):
        _str = "Uint8ArdomValuesObj012345679BCDEFGHIJKLMNPQRSTWXYZ_cfghkpqvwxyz~"
        FKGJ = ''
        for i in range(21):
            FKGJ += random.choice(_str)
        return FKGJ

    def unsigned_value(self, value, num):
        unsigned_ = value & 0xFFFFFFFF
        result = unsigned_ >> num
        result = (result + (1 << 31)) % (1 << 32) - (1 << 31)
        return result

    def CT(self, e, n, r=None):
        t = [
            "",
            " ",
            "  ",
            "   ",
            "    ",
            "     ",
            "      ",
            "       ",
            "        ",
            "         "
        ]
        e = str(e)
        n -= len(e)
        if n <= 0:
            return e
        if r is None or r == "":
            r = " "
        if r == " " and n < 10:
            return t[n] + e
        o = ""
        while n:
            o += r
            n >>= 1
            r += r
        return o + e

    def base64_encode(self, e):
        MT = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
              'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
              'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+',
              '/']
        IT = {
            "+": "-",
            "/": "_",
            "=": ""
        }
        o = ""
        i = len(e)
        a = 0
        u = 3 * (i // 3)
        a = 0
        while a < u:
            t = ord(e[a])
            n = ord(e[a + 1])
            r = ord(e[a + 2])
            o += MT[self.unsigned_value(t, 2)] + MT[63 & (t << 4 | self.unsigned_value(n, 4))] + MT[
                63 & (n << 2 | self.unsigned_value(r, 6))] + MT[63 & r]
            a += 3
        c = i - u
        if c == 1:
            t = ord(e[a])
            o += MT[self.unsigned_value(t, 2)] + MT[(t << 4) & 63] + "=="
        elif c == 2:
            t = ord(e[a])
            n = ord(e[a + 1])
            o += MT[self.unsigned_value(t, 2)] + MT[63 & (t << 4 | self.unsigned_value(n, 4))] + MT[(n << 2) & 63] + "="
        return o.translate(str.maketrans(IT))

    def charCode(self, e):
        n = []
        r = 0
        o = 0
        for o in range(len(e)):
            i = ord(e[o])
            if 0 <= i <= 127:
                n.append(i)
                r += 1
            elif 2048 <= i <= 55295 or 57344 <= i <= 65535:
                r += 3
                n.append(224 | (i >> 12) & 15)
                n.append(128 | (i >> 6) & 63)
                n.append(128 | (i) & 63)
        for a in range(len(n)):
            n[a] &= 255
        if r <= 255:
            return [0, r] + n
        else:
            return [r >> 8, 255 & r] + n

    def es(self, e):
        if not e:
            e = "undefined"
        n = []
        r = self.charCode(e)[2:]
        o = self.enn(len(r))
        n.extend(self.enn(241) + o + r)
        return n

    def en1(self, e):
        if not e:
            e = 0
        n = int(e)
        return [239] + self.enn(n)

    def en(self, e):
        if not e:
            e = 0
        n = int(e)
        r = []
        if n > 0:
            r.append(0)
        else:
            r.append(1)
        o = bin(abs(n))[2:]
        while len(o) % 8 != 0:
            o = "0" + o
        a = len(o) // 8
        for u in range(a):
            c = o[8 * u: 8 * (u + 1)]
            r.append(int(c, 2))
        r[0] = len(r)
        return r

    def sc(self, e):
        if not e:
            e = ""
        return self.charCode(e)[2:]

    def nc(self, e):
        if not e:
            e = 0
        n = abs(int(e))
        o = bin(n)[2:]
        r = len(o) // 8
        o = self.CT(o, 8 * r, "0")
        i = []
        for a in range(r):
            u = o[8 * a: 8 * (a + 1)]
            i.append(int(u, 2))
        return i

    def enn(self, e):
        if not e:
            e = 0
        n = int(e)
        r = n << 1 ^ n >> 31
        o = bin(r)[2:]
        o = self.CT(o, 7 * math.ceil(len(o) / 7), '0')
        i = []
        a = len(o)
        while a >= 0:
            u = o[a - 7: a]
            if r & -128 == 0:
                i.append("0" + u)
                break
            i.append("1" + u)
            r = self.unsigned_value(r, 7)
            a -= 7
        return list(map(lambda e: int(e, 2), i))

    def ecl(self, e):
        n = []
        r = list(bin(e)[2:])
        while len(r) < 16:
            r.insert(0, '0')
        r = ''.join(r)
        n.extend([int(r[0:8], 2), int(r[8:16], 2)])
        return n

    def get_data(self, ua):
        rand_h = random.randint(700, 2000)
        rand_w = random.randint(1100, 2000)
        fe_data_1 = [
            "Google Inc. (NVIDIA)",
            "Google Inc. (Google)",
            "Google Inc. (Intel Open Source Technology Center)",
            "Google Inc. (NULL)",
            "Intel Open Source Technology Center",
            "Google Inc. (Intel)",
            "Google Inc. (AMD)",
            "Google Inc. (NVIDIA Corporation)",
            "Google Inc. (ATI Technologies Inc.)",
            "Google Inc.",
            "Google Inc. (Unknown)",
            "Google Inc. (Apple)",
            "Google Inc. (VMware)",
            "Intel Inc.",
            "Google Inc. (Intel Inc.)",
            "Google Inc. (ARM)",
            "Google Inc. (Microsoft)",
        ]
        fe_data_2 = [
            "ANGLE (Intel, Intel(R) HD Graphics 3000 Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA Corporation, NVIDIA GeForce GT 650M OpenGL Engine, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Radeon RX550/550 Series Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD Radeon R7 350 Series Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel, Mesa Intel(R) UHD Graphics 630 (CML GT2), OpenGL 4.6)",
            "ANGLE (Intel, Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0, nvumdshimx.dll)",
            "ANGLE (NVIDIA GeForce GT 705 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 650 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA GeForce RTX 3050 Ti Laptop GPU Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 745 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro M2000M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 SUPER Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 650 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA NVS 5100M Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (ATI Technologies Inc., AMD Radeon HD 6770M OpenGL Engine, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD Radeon RX 580 2048SP Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA GeForce GT 610 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel, Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (AMD, AMD Radeon(TM) Vega 10 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 5500 Direct3D9Ex vs_3_0 ps_3_0, nvumdshimx.dll)",
            "ANGLE (NVIDIA, NVIDIA T1000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(TM) Pro Graphics 6200 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 670 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "Intel Iris OpenGL Engine",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics 650, OpenGL 4.1)",
            "ANGLE (ATI Technologies Inc., AMD Radeon Pro 560X OpenGL Engine, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 3000 Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (Intel, Intel(R) HD Graphics 3000 Direct3D9Ex vs_3_0 ps_3_0, nvumdshim.dll)",
            "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)",
            "ANGLE (NVIDIA, NVIDIA GRID M10-1B Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) Vega 3 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX 570 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (ATI Technologies Inc., AMD Radeon RX Vega 64 OpenGL Engine, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) Iris(R) Xe Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon R5 340 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 510 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, ATI Radeon 3000 Direct3D9Ex vs_3_0 ps_3_0, atiumd64.dll)",
            "ANGLE (AMD Radeon R7 Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, AMD Radeon Pro W5500 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 with Max-Q Design Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 600 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, Radeon(TM) RX Vega 10 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon (TM) R9 200 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(R) Plus Graphics 645 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX 550 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3090 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics 5300 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA Quadro K620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumdx32.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 940MX Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro K6000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti with Max-Q Design Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (ATI Technologies Inc., AMD Radeon RX 6600 XT OpenGL Engine, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(R) Plus Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-25.20.100.6472)",
            "ANGLE (Intel, Intel(R) UHD Graphics 750 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 610 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3090 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics P530 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA D10M2-20 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (AMD, AMD Radeon (TM) RX 580X Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD Radeon (TM) Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 950 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (ATI Mobility Radeon HD 5470         Direct3D9Ex vs_3_0 ps_3_0)",
            "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 505 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 710 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon R7 350 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 5300 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 6900 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA Quadro K1000M Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(TM) Graphics 5100 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 965M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 960 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon(TM) Vega 8 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 610 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro 600 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Direct3D9Ex vs_3_0 ps_3_0, nvumdshimx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 440 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(TM) Graphics 550 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)",
            "ANGLE (Intel, Intel(R) HD Graphics 510 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (NVIDIA GeForce GTX 1650 SUPER Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce 8400 GS     Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 610M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 730 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 220   Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (AMD, Radeon (TM) RX 470 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 770 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (ATI Technologies Inc., AMD Radeon RX 6600 OpenGL Engine, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA Quadro K2000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) Iris(TM) Pro Graphics 5200 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, AMD Radeon(TM) RX Vega 11 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 5000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (ATI Technologies Inc., AMD Radeon VII OpenGL Engine, OpenGL 4.1)",
            "ANGLE (Intel, Mesa Intel(R) HD Graphics 530 (SKL GT2), OpenGL 4.6)",
            "ANGLE (NVIDIA, NVIDIA GeForce 805A Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro K3000M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (ATI Technologies Inc., AMD Radeon Pro 5300 OpenGL Engine, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) Iris(R) Graphics 550 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro P600 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (AMD, AMD Radeon R7 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics 610 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) R7 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 730  Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.100.9805)",
            "ANGLE (AMD, Radeon (TM) RX 470 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro 5000  Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 705 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce MX110 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon Pro 450 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 1030 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 675MX Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) G41 Express Chipset (Microsoft Corporation - WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0, igdumd32.dll)",
            "ANGLE (NVIDIA, NVIDIA Quadro 600  Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon R7 200 Series Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTS 250 Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "ANGLE (Intel, Intel(R) G41 Express Chipset Direct3D9Ex vs_3_0 ps_3_0, igdumdx32.dll)",
            "ANGLE (VMware, VMware SVGA 3D Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "ANGLE (Intel, Mobile Intel(R) 4 Series Express Chipset Family Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)",
            "Intel(R) UHD Graphics 630",
            "ANGLE (AMD, AMD Radeon(TM) Vega 9 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 4400 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 3GB Direct3D9Ex vs_3_0 ps_3_0, nvd3dum.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 740 Direct3D9Ex vs_3_0 ps_3_0, nvd3dum.dll)",
            "ANGLE (Intel, Intel(R) HD Graphics 520 Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (Intel, Intel(R) HD Graphics P3000 Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)",
            "ANGLE (AMD, AMD Radeon(TM) Vega 6 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 730 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 610 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD Radeon(TM) R7 Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D9Ex vs_3_0 ps_3_0, nvumdshimx.dll)",
            "ANGLE (AMD, Radeon Pro 560X Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX Vega M GL Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (AMD, AMD Radeon RX 5600 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 SUPER Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 970M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 6600 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) RX Vega 10 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (Intel(R) HD Graphics 5000 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA Quadro P620 Direct3D11 vs_5_0 ps_5_0, D3D11-26.21.14.4250)",
            "ANGLE (AMD, AMD Radeon(TM) Vega 10 Mobile Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon (TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA Corporation, NVIDIA GeForce GT 755M OpenGL Engine, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "no_fp",
            "ANGLE (NVIDIA, NVIDIA Quadro P2000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD FirePro W5000 Direct3D9Ex vs_3_0 ps_3_0, aticfx32.dll)",
            "ANGLE (Google, Vulkan 1.2.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver)",
            "ANGLE (AMD Radeon(TM) R4 Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D9Ex vs_3_0 ps_3_0, nvd3dum.dll)",
            "ANGLE (AMD, AMD Radeon RX 6800 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Inc., Intel(R) HD Graphics 6000, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) Iris(R) Plus Graphics 655 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 1010 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 4080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 6750 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 950 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 525M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 3GB Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 5GB Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro P4200 with Max-Q Design Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 9500 GT Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "Mali-G71",
            "ANGLE (AMD, AMD Radeon R7 200 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 240 Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (Intel Inc., Intel(R) HD Graphics 630, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA RTX A2000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 4600 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (AMD, Radeon RX 350 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX 550X Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D9Ex vs_3_0 ps_3_0, aticfx32.dll)",
            "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro 2000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon HD 8330 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon Pro Vega 56 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0)",
            "ANGLE (NVIDIA, NVIDIA Quadro K2200 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD Radeon HD 6700 Series Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA Quadro K620 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3070 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) Iris(R) Plus Graphics 645 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce G205M  Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro P600 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA NVS 510 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (AMD, AMD Radeon (TM) R7 350 Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 650M Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (NVIDIA, NVIDIA RTX A2000 12GB Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD Radeon HD 8650G + 8570M Dual Graphics Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA Quadro P620 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, AMD Radeon R7 Graphics Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (AMD, AMD Radeon (TM) R9 380 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(R) Plus Graphics 640 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA GeForce GTX 1650 Ti Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel, Intel(R) Iris(R) Graphics 540 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 5700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 6700 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX 580 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 525M     Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (AMD 760G Direct3D9Ex vs_3_0 ps_3_0)",
            "ANGLE (NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, Radeon RX 560 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, nvumdshimx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce 310M                 Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (NVIDIA GeForce 940M Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, AMD Radeon Pro 5500M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Inc., Intel(R) Iris(TM) Graphics 540, OpenGL 4.1)",
            "ANGLE (Intel(R) UHD Graphics 610 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 640  Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 460 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "Adreno (TM) 512",
            "ANGLE (AMD, Radeon(TM) RX 460 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 920MX Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 850M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 615 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Inc., Intel(R) HD Graphics 530, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3080 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 730   Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon R9 200 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro P4000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce G210M  Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (AMD, Radeon (TM) RX 480 Graphics Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 130M  Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) R7 360 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) R6 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 617 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 830M  Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) R2 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) R3 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX550/550 Series (POLARIS12), OpenGL 4.6)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 740 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) Vega 8 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (VMware, VMware SVGA 3D Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (Unknown, Parallels Display Adapter (WDDM) Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) UHD Graphics 730 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel, Intel(R) Q45/Q43 Express Chipset Direct3D9Ex vs_3_0 ps_3_0, igdumdx32.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce 210  Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (AMD, AMD Radeon(TM) Vega 2 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D9Ex vs_3_0 ps_3_0, nvd3dum.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 650M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon (TM) R7 360 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Mobile Intel(R) 4 Series Express Chipset Family Direct3D9Ex vs_3_0 ps_3_0, igdumdx32.dll)",
            "ANGLE (Intel, Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)",
            "ANGLE (NVIDIA, NVIDIA NVS 300 Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "Google SwiftShader",
            "ANGLE (Intel, Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (AMD, Radeon RX480 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro K600  Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon PRO W6600 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Mobile Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll)",
            "ANGLE (NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, ATI Radeon HD 3450 Direct3D9Ex vs_3_0 ps_3_0, atiumd64.dll)",
            "Mali-T624",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2080 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(TM) Plus Graphics 640 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics 4000 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, Radeon RX 570 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon R5 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, ATI Mobility Radeon HD 4650 (Microsoft Corporation WDDM 1.1)  Direct3D9Ex vs_3_0 ps_3_0, atiumdag.dll)",
            "ANGLE (AMD, Radeon (TM) Pro WX 4100 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 605 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTS 450 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon Pro 5600M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2070 Super Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Unknown, Qualcomm(R) Adreno(TM) 8cx Gen 3 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 615 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 3000 Direct3D9Ex vs_3_0 ps_3_0, igdumd64.dll)",
            "ANGLE (AMD, AMD Radeon RX 6500 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics 645, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) HD Graphics 6000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Inc., Intel HD Graphics 5000 OpenGL Engine, OpenGL 4.1)",
            "Mali-G610 MC6",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 960M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics Direct3D9Ex vs_3_0 ps_3_0, igdumd32.dll)",
            "ANGLE (NULL, RDPDD Chained DD Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (AMD, AMD Radeon (TM) R9 Fury Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GRID T4-2Q Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 5700 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 660 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Open Source Technology Center, Mesa DRI Intel(R) HD Graphics 3000 (SNB GT2), OpenGL 3.3)",
            "Adreno (TM) 630",
            "ANGLE (Intel Inc., Intel(R) Iris(TM) Plus Graphics 640, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA GeForce 310M Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro 1000M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 405 Direct3D11 vs_4_1 ps_4_1, D3D11)",
            "ANGLE (Intel, Intel(R) UHD Graphics 630, OpenGL 4.5.0)",
            "ANGLE (Intel, Intel(R) HD Graphics 515 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2080 SUPER Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce G 105M Direct3D11 vs_4_0 ps_4_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0, igdumdim32.dll)",
            "ANGLE (AMD, AMD Radeon R7 430 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 650M  Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (Intel(R) Iris(TM) Graphics 5100 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 620  Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 430 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon 520 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 780 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 615 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 625 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) Iris(TM) Graphics 6100 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon Pro 555X Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 640 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 10.0.0) (0x0000C0DE)), SwiftShader driver)",
            "ANGLE (AMD Radeon HD 7000 series Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Intel Inc., Intel(R) Iris(TM) Graphics 6100, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) HD Graphics 520 Direct3D9Ex vs_3_0 ps_3_0, aticfx32.dll)",
            "ANGLE (NVIDIA Quadro K620 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA Corporation, NVIDIA GeForce GT 750M OpenGL Engine, OpenGL 4.1)",
            "ANGLE (VMware, VMware SVGA 3D Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 530 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA Quadro K2100M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Inc., Intel HD Graphics 4000 OpenGL Engine, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX 470 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA Quadro T1000 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 610 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 with Max-Q Design Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA T400 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2080 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA GeForce GT 720 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, Radeon Pro 555 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, Radeon RX 5500 XT Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD Radeon HD 7560D Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 860M Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (AMD Radeon R5 220 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (NVIDIA, NVIDIA NVS 5400M Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 520M                               Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics 4000 Direct3D9Ex vs_3_0 ps_3_0)",
            "ANGLE (AMD, AMD Radeon HD 5800 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel(R) HD Graphics 4600 Direct3D9Ex vs_3_0 ps_3_0)",
            "ANGLE (AMD, AMD RADEON R9 M395 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon HD 7700 Series Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3050 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD, AMD Radeon RX 580 2048SP Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel, Intel(R) HD Graphics 5500 Direct3D9Ex vs_3_0 ps_3_0, aticfx64.dll)",
            "ANGLE (Intel(R) HD Graphics 6000 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (AMD, AMD Radeon HD 5700 Series Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 550 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (ATI Technologies Inc., AMD Radeon Pro 555 OpenGL Engine, OpenGL 4.1)",
            "ANGLE (Intel, Intel(R) Iris(TM) Graphics 5100 Direct3D9Ex vs_3_0 ps_3_0, igdumdim64.dll)",
            "ANGLE (Intel, Mesa Intel(R) UHD Graphics 630 (CFL GT2), OpenGL 4.6)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 780 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 2060 Direct3D9Ex vs_3_0 ps_3_0, nvldumdx.dll)",
            "ANGLE (ATI Technologies Inc., AMD Radeon Pro 560 OpenGL Engine, OpenGL 4.1)",
            "ANGLE (NVIDIA Corporation, Quadro T2000 with Max-Q Design/PCIe/SSE2, OpenGL 4.5.0)",
            "ANGLE (AMD, AMD Radeon(TM) RX Vega11 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 750M    Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (AMD Radeon R5 235 Direct3D11 vs_5_0 ps_5_0)",
            "ANGLE (Apple, Apple M1, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA GeForce GT 630 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (Intel Open Source Technology Center, Mesa DRI Intel(R) HD Graphics 620 (KBL GT2), OpenGL 4.6)",
            "ANGLE (Apple, Apple M1 Max, OpenGL 4.1)",
            "ANGLE (NVIDIA, NVIDIA RTX A2000 8GB Laptop GPU Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Ti Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 9600M GT Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll)",
            "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D9Ex vs_3_0 ps_3_0, nvumdshimx.dll)",
            "ANGLE (NVIDIA, NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0, D3D11)",
            "ANGLE (NVIDIA, NVIDIA GeForce 9300 GE Direct3D11 vs_4_0 ps_4_0, D3D11)"
        ]
        fe_1 = random.choice(fe_data_1)
        fe_2 = random.choice(fe_data_2)
        ua_data = {
            "ua": ua,
            "touchSupport": [0, False, False], "osCpu": "", "language": "zh-CN", "colorDepth": 24, "deviceMemory": 8,
            "screenResolution": [2560, 1440], "availableScreenResolution": [2560, 1400], "hardwareConcurrency": 24,
            "timezoneOffset": -480, "timezone": "Asia/Shanghai", "cpuClass": "not available", "platform": "Win32",
            "cookiesEnabled": True, "webdriver": "not available", "addBehavior": False, "plugins": [
                ["Chrome%20PDF%20Viewer", "Portable%20Document%20Format",
                 [{"type": "application%2Fpdf", "suffixes": "pdf"}, {"type": "text%2Fpdf", "suffixes": "pdf"}]],
                ["Chromium%20PDF%20Viewer", "Portable%20Document%20Format",
                 [{"type": "application%2Fpdf", "suffixes": "pdf"}, {"type": "text%2Fpdf", "suffixes": "pdf"}]],
                ["Microsoft%20Edge%20PDF%20Viewer", "Portable%20Document%20Format",
                 [{"type": "application%2Fpdf", "suffixes": "pdf"}, {"type": "text%2Fpdf", "suffixes": "pdf"}]],
                ["PDF%20Viewer", "Portable%20Document%20Format",
                 [{"type": "application%2Fpdf", "suffixes": "pdf"}, {"type": "text%2Fpdf", "suffixes": "pdf"}]],
                ["WebKit%20built-in%20PDF", "Portable%20Document%20Format",
                 [{"type": "application%2Fpdf", "suffixes": "pdf"}, {"type": "text%2Fpdf", "suffixes": "pdf"}]]],
            "sessionStorage": True, "localStorage": True, "indexedDb": True, "openDatabase": True,
            "vendor": fe_1,
            "windowAllSize": {"h": [rand_h - 130, rand_h], "w": [rand_w, rand_w - 16], "dh": 130, "dw": 16}
        }
        ea = str(int(time.time() * 1000))
        FKGJ = self.get_FKGJ()
        hj_data = {"chrome": "true", "cef": "udf", "miniblink": "udf", "navigator": "udf", "electron": "true",
                   "unknowChrome": {"runtime": "true", "brands": "false", "version": "false", "webviewName": "false",
                                    "wke": "false", "ua": "false", "_process": "false", "_prompt": "true"}}
        ue_1 = self.es("isInterval")
        ue_2 = self.es("false")
        ue_3 = self.es("rawData")
        ue_4 = self.es(json.dumps(ua_data, separators=(',', ':'), ensure_ascii=False))
        ue_5 = self.es("localIp")
        ue_6 = self.es("0.0.0.0")
        ue_7 = self.es("reportTimestamp")
        ue_8 = self.es(ea)
        ue_9 = self.es("version")
        ue_10 = self.es("2.3.6")
        ue_11 = self.es("app")
        ue_12 = self.es("h5Market")
        ue_13 = self.es("FKGJ")
        ue_14 = self.es(FKGJ)
        ue_15 = self.es("uid")
        ue_16 = self.es("")
        ue_17 = self.es("hasCdc")
        ue_18 = self.es("false")
        ue_19 = self.es("electronCef")
        ue_20 = self.es(json.dumps(hj_data, separators=(',', ':'), ensure_ascii=False))
        ue_21 = self.es("frontReferer")
        ue_22 = self.es("")
        ue = ue_1 + ue_2 + ue_3 + ue_4 + ue_5 + ue_6 + ue_7 + ue_8 + ue_9 + ue_10 + ue_11 + ue_12 + ue_13 + ue_14 + ue_15 + ue_16 + ue_17 + ue_18 + ue_19 + ue_20 + ue_21 + ue_22
        ce = []
        xe_data = {"gyroFlag": False, "acceFlag": False}
        xe = self.es("hasSensor") + self.es(json.dumps(xe_data, separators=(',', ':'), ensure_ascii=False))
        se = self.es("isFront") + self.es("true")

        fe_data = [fe_1, fe_2, "WebKit", "WebKit WebGL", "WebGL 1.0 (OpenGL ES 2.0 Chromium)"]
        fe = self.es("webGLInfos") + self.es(json.dumps(fe_data, separators=(',', ':'), ensure_ascii=False))
        le_data = [rand_w, rand_h]
        le = self.es("windowSize") + self.es(json.dumps(le_data, separators=(',', ':'), ensure_ascii=False))
        de = self.es("chromium") + self.es("false")
        ve = self.es("headlessByProperties") + self.es("true")
        he = self.es("winSelenium") + self.es("false")
        pe_data = ["zh-CN", "zh"]
        pe = self.es("languages") + self.es(json.dumps(pe_data, separators=(',', ':'), ensure_ascii=False))
        me = self.es("consoleLied") + self.es("false")
        ge_data = []
        ge = self.es("injectScripts") + self.es(json.dumps(ge_data, separators=(',', ':'), ensure_ascii=False))
        rps = f'100{random.randint(20, 99)}'
        r_pid = f'6010{random.randint(10000, 99990)}{random.randint(100000, 999900)}'
        Ee_data = [f"https://apps.apple.com/kr/app/id16{random.randint(10000000, 99990000)}?rps={rps}&r_pid={r_pid}",
                   f"https://play.google.com/store/apps/details?id=com.einnovation.temu&hl=ko&gl=kr&rps={rps}&r_pid={r_pid}",
            "https://www.instagram.com/temu/",
            "https://www.facebook.com/shoptemu/",
            "https://www.twitter.com/@shoptemu",
            "https://www.tiktok.com/@shoptemu",
            "https://www.youtube.com/@temu",
            "https://www.pinterest.com/shoptemu/",
            "https://aimg.kwcdn.com/material-put/1e14dde07df/eb70f7c5-9848-4355-a7ac-827eae894571.png?imageView2/2/w/300/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/52192109-d0ca-4e0a-86ac-902be3d9fe23.png.slim.png?imageView2/2/w/100/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/86987e2c-6cfc-4955-b816-11fca50f795f.png.slim.png?imageView2/2/w/100/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/pintu/7c2ba34f-7e25-42b2-9df3-a33c20a08c56.png?imageView2/2/w/100/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/promotion/6af2782d-94e4-4106-b081-8d7ba6c15c84.png.slim.png?imageView2/2/w/100/q/70/format/webp",
            "https://dl.kwcdn.com/upload-common/commodity/c8b30c5b-0d15-4800-a24f-f97879ac6fdc.png?imageView2/2/w/120/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/openingemail/flags/e9c2ade0-f09a-40d3-80c8-925fd5ed1ba8.png.slim.png?imageView2/2/w/48/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/324fa52e7e92059fdf0a145e28747dfc.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-09-13/1694624420560-3083ee375fad471a9534b0abdfb31e46-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/751da10a9d66019fe233fe8b545927f9.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/828e6bea8f11c2741f8b1044cda34f9c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2022-12-27/1672158683199-d19b059e718f46cb8e0d72cca5147b20-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/fa9d3105418cc22d9d8c0326ccf06d0c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-02-27/1677504137670-237a8312bdf24d83959ba19447b2cfec-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/86524b0f48062448e0a64059bf18dbf6.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/d7a0210102a0688accb572d3caf7b282.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-02-11/1676095995789-d6fb59f522fc4cd9a80855c9484bf872-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/2a52bd4ecc6398a47f6b06b3097c14c2.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/c9a0f78c0fbda987bb0125b8d82a1aed.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/fancyalgo/toaster-api/toaster-processor-image-cm2in/68033bb8-5ba5-11ee-a5e1-0a580a69767f.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-06-01/1685610407803-a81a4e1faba349e79e4b5752c76d5dde-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/3eafd4050501f9f4d4505c48be470188.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/eea334eecf7254988dbb3786132b63d0.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/91b6bda417220d32f9d73f543d30b97b.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-07-03/1688358193840-9c3cb42fc99a4ff48d2f825227b987a5-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/10e1a1bc5c4ef3049cb271062dcbdd28.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2022-11-30/1669788220941-d8fd98ad0627475985b72a5cba730474-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/1b7be55cbe09ce3b806ec03807b35772.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg_b/lightningdeal/3bcc7ad7-9edd-442b-a8a2-7324ca27f2d9.png?imageView2/2/w/512/q/100/format/webp",
            "https://img.kwcdn.com/product/1d14c6c03de/167fa33a-9981-4baf-8fc8-7fd18a3e359f_1000x1000.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-04-25/1682436965800-79ad0e393dff4371900c9b8dab187ebf-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/51cede657df4f40766bdd27994dd50e4.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/c533fca73b6c704a2133faab1cf060d3.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-07-06/1688605937432-673b747270614796b302a42c64c56841-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-05-08/1683524104089-8b126ebd6e94435f952bda411816f05b-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/415004478beb6b08b94970f6b290166b.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/cced2520b3d0de8d50427d9f73a6530a.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-06-21/1687362123375-09fa6d900a084a92afb59583d875386b-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/dc83fc90e3bf1046e96b1a6fd6d4759c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-07-22/1689997835069-402d83ba274047d8b9596ec3f32b5308-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/c11056d6987b51137f11e17102c9b7bb.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-06-13/1686640377606-e0a9c8907b0f4ce0b43909a4b3308b90-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/72e22f781f8ad473cb5572a67ec7884d.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/74585da0588cc069aa686b0c911c6a7e.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2022-12-27/1672123928332-ae844c56698845afb2b8aa8acf0e7e1e-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/c8927e6159ce6745c4521ed590356d05.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/720477bcd83fd686a1e0be5d53413580.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-09-15/1694745612951-4fd9d28161e94d28a10d1d971acef3c7-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-04-08/1680940374384-4b9c5358431f4ec483dbb9102b90c6ff-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/1d14c6c0898/80c9d0cd-f0d7-4524-8ca4-efb9a4ff0204_1200x1200.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/8fd83df27919310b148aa93c0f1f8e5e.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/eb4dd9bb313b7ce58617bb20f4cde0ce.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/1d18fce1770/ffa5df97-b63c-4134-94b1-7911b78fcc55_1298x1298.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/75802e6e58fd3ee24d5d3c44ee421137.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/b1579a9821876572f53ecdd7800b88eb.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/f256b3c622b60be64e07bd2fb8e3e16b.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/9bb2c06eb0a955ef8e626dbc5b78401f.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/5b18dafe7f99f2cbce5e196da3e50f70.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/38215dec73d393b278feae44ad4e3cd6.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/5878ecaaf096cb098aec08c81eaaf03b.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/fda5ea44f70fd1779d9a63d8d6a373f4.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/cf1f6c4abd5b1f2bbf7e6a608a9f7ae7.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/472c106aa25e513185de03ecb45f5181.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/a2e16851ad6653e18f48e347efb4b74c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-02-25/1677320790377-8b61ba2fd6244e83a3570625daf086e8-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/31fa4de3f2b2eaf6885a3cc304a6775a.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-05-05/1683275624071-1e45063c7c784d9595ad89615a29a237-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/e56af2e260c0b71d05a07bbc4d2e81cf.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-05-23/1684852457903-28650ffd13c14a388e9de2f13693d99e-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/25b3ee1480eaff9aa6725d26e49b483f.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/af25f0283fad60868d8b0279325bf40c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/834010dfc27b0dfcfe56530bf885e2b3.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/b202a1b11feaf99d4c70c69f71870de4.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-04-29/1682782364613-ac894017c3364a65bd23a8d7fe2aec09-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/f7c96595f5d83479a0d69874acfe1219.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-04-12/1681309389356-a54f34cdd29c4901b0db1241af4830f1-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/99a90f8b872a1cbc9d6c3ca87bc5953d.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/aebfc4a909b5767743431fca0565eee5.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/8ead9360395b4556a7bd63ada7cb6431.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/2d6e9f3272aa79aefed17668d9d46d45.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-05-10/1683700298370-4a739692d832453c891b4b9e2935fee4-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/5c73df5433ea3324404ffb3724279302.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/2412cb9c6ff2291c315fccfa17dc1c01.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-07-03/1688365464063-42c72bc333de4516923cda71a5b37b92-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/dc2400089a39632c94bef0665b0f67ac.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/1a8716f965ffb32ca89a277220ba6cd2.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-05-25/1684985238219-3234ed362c004616ab49fa8f14617884-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/8511ff1579f2d22f52270c31e3f4155d.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/9fc469d8fb3b0c0a389fc76f796d6539.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/8351f6568e3d8d4844150b2c270db2a2.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/40efad3ce8315fa6d29624afb15a315d.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/e5a02dad75fdb056c80a6d12d0d4d1d5.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/4765fa675b17ac9f60490b7f8a952ea0.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/b1a77b40d6534b1b60836894e7ec4804.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/603bfe83648165c054cc653585c7bac4.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2022-11-30/1669778502140-a7742fad38a24cdc9e18e5facc96f388-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/9effce042f11e38b98ed37ebca300bd1.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/1310efedd65d2c8e07f5cbb39ec96d58.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/b8876c5fbd991e7244924661e44876f5.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/c3d6b995898b3ae84e72c702098afbc9.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/099981e7e015334bd875ef976f734fef.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2022-11-28/1669603770397-5c3c1cf1026448a89800d54c11fe191d-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-06-14/1686724896049-3eb4ab32701b4e88b40b567af55b45b0-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/1a5118a87f740beef007a1fc90c7c246.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-06-07/1686123547304-a41ec078094e42468516c3a36e4088de-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/e54f51b477d7b0783162139a5ebd0cb4.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/179d38e6dcb15c1d49d632ff7c28d8c8.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/7c6d4a650659115e8af08f02fdbf3a88.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/0d1eef47dd92f02758ae397b4e5042fa.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/74394694219e7538733f3d9707121031.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/55589702d60f24acc76f6ec2610a34dc.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-03-16/1678975057127-44e8a3fa9caa494e842787b6a9220a9e-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/68f019fdd040d99349c58dda9d83487a.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/70340adc9abe68d8a8d07e7a7f5b4b92.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/6eb866ed3e243bf12df13bb3ddd3d376.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/a6096c50e75867ba8c7561f525f5ec39.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-06-28/1687938681069-1f205e51dd9b484c8c3a66db277dddde-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/3fc03b8fa1e008c9f9551f953aab39c7.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/d6033ff19e55ad562e577c8c947cce82.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/b3c94d19af5fa1f1b1d0338593c3c1b9.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/399bcd6321d8d205d686d7c02f41cf8a.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/0e7382b6c9def21db7a01e67f7a0ead0.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/2354c8d54149b77dea4fb122f585fe8c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2023-01-22/1674404120018-2c8d6a4261584090a88a07364591f678-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/45a53bad0dd5a4f8a2ed9d30ec50ca15.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/f9c9a9c6a3667a329e02a6d2b0a6ec0a.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/aaf7dcb43f6533dfdf86934544f25c72.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/acc340d68e8f25105c1371946f035acf.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/d469c9b334f666c2aa4b6e5353794b41.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/32f194a5b9aa239f92d7f9953d2c6755.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/bdfb77f94fcaa4000a2376611c8e74ae.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/5f3824af25dd5c70eb6f43e5fc963fbc.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/7988eb4c1e16b48230a3007753f325ed.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/90859c5b4903992eeacf7a23089afc5c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/6591d9b13f409d245f5c6bd5765713b1.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/aef1a48a210fd4f7ca6cb34ba2aa8b57.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/open/2022-10-31/1667204116704-e9a53dd06c084fdb83e91ca4e749dbbe-goods.jpeg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/0cd0a3fbb77377dda75c5444785bf110.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/ad2bb9f404cd95b1deb185c0836302de.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/37ae05b7aaed6ca575a82d9f9ed55e55.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/64978df43660a52c2e2f36f62f08d968.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/fancyalgo/toaster-api/toaster-processor-image-cm2in/b9ee2750-204d-11ee-acbb-0a580a69c84a.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/bf33271cae6db5cec9e954e1aa5e96d6.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/29bcfbca6cf39c247c5f13de391805fe.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/5515c904083368cb80f1b500af308e7b.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/359d76853f7dc6ba7e74532ab91dfa23.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/b5e87d965dbb56df8e895e1804ce9bea.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://img.kwcdn.com/product/Fancyalgo/VirtualModelMatting/0a430f1f36d4eb8dd6a3479fb472c94c.jpg?imageView2/2/w/500/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/pc/5c5f0a0f-db6f-4205-a0d3-c745b6c672ea.png.slim.png",
            "https://aimg.kwcdn.com/upload_aimg/pc/427c29ba-bef6-439c-9d4c-edbdde47c7e0.png.slim.png",
            "https://aimg.kwcdn.com/upload_aimg/pc/a817be22-932c-43b3-95e4-c768af711c34.png.slim.png",
            "https://aimg.kwcdn.com/upload_aimg/pc/0d1c5252-2094-4504-b6fc-34a6a3f87804.png.slim.png",
            "https://aimg.kwcdn.com/upload_aimg/temupch5/4eb16ee6-f4ed-426e-9ce3-574a2ab4ba6c.png",
            "https://aimg.kwcdn.com/upload_aimg/web/7edd0665-db19-4e7a-aa42-5301e5ea396f.png.slim.png",
            "https://aimg.kwcdn.com/upload_aimg/web/18e81de4-adca-4b74-bd52-1aa2d7ebe771.png.slim.png",
            "https://aimg.kwcdn.com/upload_aimg/web/2ba1be46-f0c5-4f59-aa05-1ab05ef41126.png.slim.png",
            "https://aimg.kwcdn.com/upload_aimg/temu/bcb8bf23-78c9-45ab-b480-f7020d1a5f66.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/28a227c9-37e6-4a82-b23b-0ad7814feed1.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/f1c00d04-7dde-4d4a-ae3d-b8aad2de8f96.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/65e96f45-9ff5-435a-afbf-0785934809ef.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/1f29a857-fe21-444e-8617-f57f5aa064f4.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/80d57653-6e89-4bd5-82c4-ac1e8e2489fd.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/52656b9f-5cb7-416f-8e12-f8cb39d3b734.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/ec0c5d69-1717-4571-a193-9950ec73c8af.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/da7f463a-916f-4d91-bcbb-047317a1c35e.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/b79a2dc3-b089-4cf8-a907-015a25ca12f2.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/936bf9dc-9bb2-4935-9c5a-a70b800d4cf1.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/3f39097d-e751-4891-af08-41b63ebc876e.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/fb599a1d-6d42-49f2-ba7a-64b16d01b226.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/c6962c14-ad79-4856-89e4-32205f96a7de.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/c3e5eb19-1b60-4c2b-87e1-4528fb390cbf.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/b60cd5f3-9c10-4d21-af26-a5b92cbce824.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/7d02a691-5391-418d-a38e-eadde739e22e.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/baacbca4-6cbb-41ce-bc81-59eab8ac3638.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/ac293ffc-9957-4588-a4df-f3397b4a54e0.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/d9faa4c2-17e6-4012-bc43-179d7252c184.png.slim.png?imageView2/2/w/800/q/70/format/webp",
            "https://aimg.kwcdn.com/upload_aimg/temu/8d57d602-98bf-4da0-b127-ff667db68fdf.png.slim.png?imageView2/2/w/800/q/70/format/webp"]
        Ee = self.es("extensionImgs") + self.es(json.dumps(Ee_data, separators=(',', ':'), ensure_ascii=False))
        Se = self.es("hookFuncs") + self.es('["Function.toString"]')
        be = self.es("elements") + self.es("{}")
        ye = []
        _e = self.es("outterJs") + self.es("{}")
        Te = self.es("cssFeatures") + self.es("2106138280")
        we_data = {"ALIASED_POINT_SIZE_RANGE": [1, 1024], "ALIASED_LINE_WIDTH_RANGE": [1, 1],
                   "STENCIL_VALUE_MASK": 2147483647,
                   "STENCIL_WRITEMASK": 2147483647, "STENCIL_BACK_VALUE_MASK": 2147483647,
                   "STENCIL_BACK_WRITEMASK": 2147483647,
                   "MAX_TEXTURE_SIZE": 16384, "MAX_VIEWPORT_DIMS": [32767, 32767], "SUBPIXEL_BITS": 4,
                   "MAX_VERTEX_ATTRIBS": 16,
                   "MAX_VERTEX_UNIFORM_VECTORS": 4096, "MAX_VARYING_VECTORS": 30,
                   "MAX_COMBINED_TEXTURE_IMAGE_UNITS": 32,
                   "MAX_VERTEX_TEXTURE_IMAGE_UNITS": 16, "MAX_TEXTURE_IMAGE_UNITS": 16,
                   "MAX_FRAGMENT_UNIFORM_VECTORS": 1024,
                   "SHADING_LANGUAGE_VERSION": "WebGL GLSL ES 3.00 (OpenGL ES GLSL ES 3.0 Chromium)",
                   "VENDOR": "WebKit",
                   "RENDERER": "WebKit WebGL", "VERSION": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
                   "MAX_CUBE_MAP_TEXTURE_SIZE": 16384, "MAX_RENDERBUFFER_SIZE": 16384,
                   "UNMASKED_VENDOR_WEBGL": fe_1,
                   "UNMASKED_RENDERER_WEBGL": fe_2,
                   "MAX_3D_TEXTURE_SIZE": 2048, "MAX_ELEMENTS_VERTICES": 2147483647, "MAX_ELEMENTS_INDICES": 2147483647,
                   "MAX_TEXTURE_LOD_BIAS": 2, "MAX_DRAW_BUFFERS": 8, "MAX_FRAGMENT_UNIFORM_COMPONENTS": 4096,
                   "MAX_VERTEX_UNIFORM_COMPONENTS": 16384, "MAX_ARRAY_TEXTURE_LAYERS": 2048,
                   "MAX_PROGRAM_TEXEL_OFFSET": 7,
                   "MAX_VARYING_COMPONENTS": 120, "MAX_TRANSFORM_FEEDBACK_SEPARATE_COMPONENTS": 4,
                   "MAX_TRANSFORM_FEEDBACK_INTERLEAVED_COMPONENTS": 120, "MAX_TRANSFORM_FEEDBACK_SEPARATE_ATTRIBS": 4,
                   "MAX_COLOR_ATTACHMENTS": 8, "MAX_SAMPLES": 16, "MAX_VERTEX_UNIFORM_BLOCKS": 12,
                   "MAX_FRAGMENT_UNIFORM_BLOCKS": 12, "MAX_COMBINED_UNIFORM_BLOCKS": 24,
                   "MAX_UNIFORM_BUFFER_BINDINGS": 24,
                   "MAX_UNIFORM_BLOCK_SIZE": 65536, "MAX_COMBINED_VERTEX_UNIFORM_COMPONENTS": 212992,
                   "MAX_COMBINED_FRAGMENT_UNIFORM_COMPONENTS": 200704, "MAX_VERTEX_OUTPUT_COMPONENTS": 120,
                   "MAX_FRAGMENT_INPUT_COMPONENTS": 120, "MAX_SERVER_WAIT_TIMEOUT": 0, "MAX_ELEMENT_INDEX": 4294967294,
                   "MAX_CLIENT_WAIT_TIMEOUT_WEBGL": 0, "antialias": True, "MAX_TEXTURE_MAX_ANISOTROPY_EXT": 16,
                   "VERTEX_SHADER.LOW_FLOAT.precision": 23, "VERTEX_SHADER.LOW_FLOAT.rangeMax": 127,
                   "VERTEX_SHADER.LOW_FLOAT.rangeMin": 127, "VERTEX_SHADER.MEDIUM_FLOAT.precision": 23,
                   "VERTEX_SHADER.MEDIUM_FLOAT.rangeMax": 127, "VERTEX_SHADER.MEDIUM_FLOAT.rangeMin": 127,
                   "VERTEX_SHADER.HIGH_FLOAT.precision": 23, "VERTEX_SHADER.HIGH_FLOAT.rangeMax": 127,
                   "VERTEX_SHADER.HIGH_FLOAT.rangeMin": 127, "VERTEX_SHADER.HIGH_INT.precision": 0,
                   "VERTEX_SHADER.HIGH_INT.rangeMax": 30, "VERTEX_SHADER.HIGH_INT.rangeMin": 31,
                   "FRAGMENT_SHADER.LOW_FLOAT.precision": 23, "FRAGMENT_SHADER.LOW_FLOAT.rangeMax": 127,
                   "FRAGMENT_SHADER.LOW_FLOAT.rangeMin": 127, "FRAGMENT_SHADER.MEDIUM_FLOAT.precision": 23,
                   "FRAGMENT_SHADER.MEDIUM_FLOAT.rangeMax": 127, "FRAGMENT_SHADER.MEDIUM_FLOAT.rangeMin": 127,
                   "FRAGMENT_SHADER.HIGH_FLOAT.precision": 23, "FRAGMENT_SHADER.HIGH_FLOAT.rangeMax": 127,
                   "FRAGMENT_SHADER.HIGH_FLOAT.rangeMin": 127, "FRAGMENT_SHADER.HIGH_INT.precision": 0,
                   "FRAGMENT_SHADER.HIGH_INT.rangeMax": 30, "FRAGMENT_SHADER.HIGH_INT.rangeMin": 31,
                   "MAX_DRAW_BUFFERS_WEBGL": 8}
        we = self.es("webglFt") + self.es(json.dumps(we_data, separators=(',', ':'), ensure_ascii=False))
        Ce_data = [0.09999990463256836, 0.10000014305114746]
        Ce = self.es("performanceTime") + self.es(json.dumps(Ce_data, separators=(',', ':'), ensure_ascii=False))
        Ae = self.es("emptyEvalLength") + self.es("33")
        Oe = self.es("errorFF") + self.es("false")
        Re = self.es("headerCache") + [226, 3, 0]
        Me = self.es("fonts") + self.es("00800041000100200000000036NaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaNNaN")
        Ie_data = {
            "audioTypes": {"audio.ogg": "probably", "audio.mp3": "probably", "audio.opus": "probably",
                           "audio.wav": "probably",
                           "audio.m4a": "maybe"}, "audioLoop": True, "history": True, "synthesis": True,
            "videoTypes": {"video.h264": "probably", "video.webm": "probably", "video.vp9": "probably"},
            "videoCrossOrigin": True, "videoLoop": True, "videoPreload": True, "inputCapture": False, "inputFile": True,
            "inputFormEnctype": True, "shadowroot": True, "geolocation": True, "download": True, "crossOrigin": True,
            "scriptDefer": True, "webCryptography": True}
        Ie = self.es("h5Features") + self.es(json.dumps(Ie_data, separators=(',', ':'), ensure_ascii=False))
        Ne = ue + ce + xe + se + fe + le + de + ve + he + pe + me + ge + Ee + Se + be + ye + _e + Te + we + Ce + Ae + Oe + Re + Me + Ie

        return Ne, ea

    def main(self, ua):
        init_data, init_time = self.get_data(ua=ua)
        compressed_data = zlib.compress(bytes(init_data))
        f = list(compressed_data)
        s = [chr(code) for code in f]
        data = "0a" + self.base64_encode(''.join(s))
        sha1_hash = hashlib.sha1()
        sha1_hash.update(("fe" + "HJ6793TJDI86DLS9D" + init_time + data).encode())
        _sign = sha1_hash.hexdigest()
        return {
            "data": data,
            "timestamp": init_time,
            "appKey": "fe",
            "sign": _sign
        }


    def get_bee(self):
        url = 'https://www.temu.com/api/phantom/xg/pfb/a4'
        headers = {
            "accept": "application/json, text/plain, */*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json;charset=UTF-8",
            "origin": "https://www.temu.com",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-Dest": "empty",
            "sec-fetch-Mode": "cors",
            "sec-fetch-Site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }
        data = self.main(ua=headers["user-agent"])
        proxy = http_form_data(data=get_proxies())
        res = requests.get(url="http://localhost:6666/fetch?url=" + url, data={
                  "method": "POST",
                  "header": http_form_data(data=headers),
                  "cookie": '',
                  "body": '',
                  "json": http_form_data(data=data),
                  "timeout": 30,
                  "proxy": proxy
        })
        print(res.headers["Set-Cookie"])
        cookies_iteam = res.headers["Set-Cookie"].split('; ')
        cookies = {}
        for i in cookies_iteam:
            it = i.split('=')
            cookies[it[0]] = it[1]
        print(cookies)
        return cookies

@vthread.pool(2)
def tex(ii):
        url = "https://www.temu.com/g-601099513396749.html"
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
        }

        bee_encode_obj = BeeEncode()
        cookies = {
                    'region': '211',
                    'language': 'en',
                    'currency': 'USD',
                    'timezone': 'Asia%2FShanghai',
                    'webp': '1',
                    'shipping_city': '211',
                }
        cookies.update(dict(bee_encode_obj.get_bee()))
        params = {
            'refer_page_id': f'100{random_str(slat=string.digits, length=2)}_{int(time.time())}_{random_str(slat=string.digits + string.ascii_lowercase, length=10)}',
        }
        url = url + '?' + http_pramas(data=params)
        proxy = http_form_data(data=get_proxies())

        res = requests.get(url="http://localhost:6666/fetch?url=" + url, data={
                  "method": "GET",
                  "header": http_form_data(data=headers),
                  "cookie": http_form_data(data=cookies),
                  "body": '',
                  "json": '',
                  "timeout": 30,
                  "proxy": proxy
        })
        if len(str(res.text)) > 700000:
            logger.info(f"{len(res.text)}, {'True'}")
        else:
            logger.error(f"{len(res.text)}, {'False'}")

        # if len(_res.text) > 600000:
        #     open("detail.html", "wb+").write(_res.text.encode('utf-8'))


for i in range(1):
    tex(i)


