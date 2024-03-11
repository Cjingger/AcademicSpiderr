# !/usr/bin/python3
# -*- coding:utf-8 -*-
import re, time

from utils import redisUtil
from ast import literal_eval

_redis = redisUtil.RedisUtil()

def opera_coo(coo: str, name):
    coo_dict = {}
    for c in coo.split("; "):
        coo_dict[c.split("=")[0]] = c.split("=")[1]
    _redis.redis_db.sadd(name, str(coo_dict))
    # _redis.redis_db.setex(name, 99999, str(coo_dict))
    print("cookie add success")

def pop_coo(name):
    coo_str = bytes.decode(_redis.redis_db.srandmember(name))
    coo_dict = {}
    for c in coo.split("; "):
        coo_dict[c.split("=")[0]] = c.split("=")[1]
    print(coo_dict)
    return coo_dict


if __name__ == '__main__':
    coo = ''
    name = 'scopus_cookie'
    # name = 'EI_cookie'
    opera_coo(coo, name)