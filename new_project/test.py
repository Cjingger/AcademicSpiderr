import asyncio
import random
import sys
from datetime import datetime, timedelta
import json
import re
import time
import urllib.parse as up
import base64
from math import floor
import numpy as np
import matplotlib.pyplot as plt

from utils import aioRedisUtil

ori = "http://www-scopus-com-443.bjmu.ilibs.cn/record/display.uri?eid=2-s2.0-85114677237&origin=resultslist&sort=plf-f&src=s&st1=Journal+Of+Supercomputing&sid=f40c42e5936a8ee860121119eda1087f&sot=b&sdt=b&sl=54&s=SRCTITLE%28Journal+Of+Supercomputing%29+AND+PUBYEAR+%3e+2020&relpos=815&citeCnt=0&searchTerm="
sid = "a4afc789579534c30a5b9adbb6e280eb"

_sid = re.findall(r"^.*?sid=(.*?)&sot=b&sdt.*?$", ori, re.I)[0]
print(_sid)
new = ori.replace(_sid, sid)
print(new)


print(int(time.time() * 1e3))

# d = "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjEyNzMxMjEiLCJhcCI6IjE1ODg3NTg5NzIiLCJpZCI6IjA3NjMwMTVkMmRiZWQ1OTUiLCJ0ciI6ImM4NDc3ODg0MzIyZTE4MmUwOTBkMTU1YjY4OWI4ZmQwIiwidGkiOjE2NzY0MjUyMjYzNTIsInRrIjoiMjAzODE3NSJ9fQ=="
# print(bytes.decode(base64.b64decode(d)))
print(bytes.decode(base64.b64decode("aHR0cDovL29ubGluZWxpYnJhcnktd2lsZXktY29tLTQ0My5jYW1zLmlsaWJzLmNuICAgIA==")))



# -*- coding: utf-8 -*-
args = ("2023-12-03 12 30 00", "2023-12-03 22 40 00")

st = datetime.strptime(args[0], "%Y-%m-%d %H %M 00")
et = datetime.strptime(args[1], "%Y-%m-%d %H %M 00")
diff = str(et - st)
print(diff)
if "day" in diff:
    d = int(re.findall(r"^(\d) day.*?", diff, re.I)[0])
    if d >= 6:
        t_gap = floor(round(d / 6, 2) * 24 * 60)
        for _ in range(6):
            _t = st + timedelta(minutes=_ * t_gap)
            print(f"{_} {_t}")
    else:
        h = int(diff.split(", ")[-1].split(":")[0])
        m = int(diff.split(", ")[-1].split(":")[1])
        total = 24 * 60 * d + 60 * h + m
        t_gap = floor(total / 6)
        for _ in range(6):
            _t = st + timedelta(minutes=_ * t_gap)
            print(f"{_} {_t}")
# diff在24小时之内
else:
    h = int(diff.split(":")[0])
    m = int(diff.split(":")[1])
    total = 60 * h + m
    t_gap = floor(total / 6)
    for _ in range(6):
        _t = st + timedelta(minutes=_ * t_gap)
        print(f"{_} {_t}")

aio_redis = aioRedisUtil.AioRedisUtil()

async def _test():
    k = await aio_redis.aredis_db.keys(pattern='*scopus:*')
    k = [bytes.decode(_).replace("scopus:", "") for _ in k]
    print(k)

def calc_benefit(base: int, year: int):
    benefit = []
    y_benefit = []
    y_mouth = []
    _base = base
    for m in range(year):
        if m == 0:
            y_mouth.append(1)
        else:
            y_mouth.append((m+1) * 12)
        y_rate = 0.028
        y_b = (base * 2 * y_rate) * (m + 1)
        y_benefit.append(y_b)
    print(y_mouth)
    print(y_benefit)
    for m in range(12 * year):
        rate = random.uniform(0.046, 0.049)
        base += round((base * rate) / 12, 4)

        benefit.append([m+1, base])
    step = 12
    benefits = benefit[0:-1:step]
    benefits.append(benefit[-1])
    plt.figure(figsize=(15, 9))
    plt.title("calc_benefit")
    __mouth = [m[0] for m in benefits]
    __b = [b[1] - _base for b in benefits]
    plt.plot(__mouth, __b, marker="o", markersize=3)
    plt.plot(y_mouth, y_benefit, marker="o", markersize=3)

    # 设置数据标签位置及大小
    for _a, _b in zip(__mouth, __b):
        plt.text(_a, _b, _b, ha='center', va='bottom', fontsize=10)
    for _a, _b in zip(y_mouth, y_benefit):
        plt.text(_a, _b, _b, ha='center', va='bottom', fontsize=10)
    plt.legend(["benefit-1", "benefit-2"])
    plt.show()
    return benefits


if __name__ == '__main__':
    # print(calc_benefit(int(1 * 1e4), 10))
    # print("now_date", int(time.time() * 1e3))
    print(int(time.time()))
    # st = datetime.strptime("2023-02-26 12:00", "%Y-%m-%d %H:%M")
    # et = datetime.strptime("2023-02-26 11:30", "%Y-%m-%d %H:%M")
    # _ = st + timedelta(hours=8)
    # _time = time.time()