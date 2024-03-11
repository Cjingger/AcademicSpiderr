# !/usr/bin/python3
# -*- coding:utf-8 -*-
import asyncio
import string
from copy import deepcopy
import httpx
import random
import openpyxl
from utils import aioRedisUtil
from utils import redisUtil
from common.tools import SSLFactory
import execjs
from aredis import pipeline
import datetime

aio_redis = aioRedisUtil.AioRedisUtil()
_redis = redisUtil.RedisUtil()

_timeout = httpx.Timeout(timeout=20, connect=15, read=16)
_limit = httpx.Limits(max_connections=200, max_keepalive_connections=150)
sslgen = SSLFactory()

proxy = {
    "http://": f"http://a364187154_{random.randint(1, 100000000)}-country-hk:a123456z@gateus.rola.info:1000",
    "https://": f"http://a364187154_{random.randint(1, 100000000)}-country-hk:a123456z@gateus.rola.info:1000"
}
with open(r"./js/ei.js", "r") as f:
    compile_js = execjs.compile(f.read())

proxy_cn = {
    "http://": "http://127.0.0.1:1080",
    "https://": "http://127.0.0.1:1080",
}

with open(r"./ip/bd.txt", "r", encoding="utf8") as f:
    ip_list = f.read()
_ip = random.choice(ip_list.split("\n")).replace("as.", "proxy.")
# _ip = "as.ipidea.io"
# _port = "2334"

# proxy_ipidea = {
#     "http://": f"http://{_ip.split(':')[2]}:{_ip.split(':')[3]}@{_ip.split(':')[0]}:{_ip.split(':')[1]}",
#     "https://": f"http://{_ip.split(':')[2]}:{_ip.split(':')[3]}@{_ip.split(':')[0]}:{_ip.split(':')[1]}"
# }
seed = "".join(random.sample(string.ascii_lowercase + string.digits, random.randint(12, 12)))
proxy_ipidea = {
    "http://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334",
    "https://": f"http://qsx_global-zone-custom-region-hk-session-{seed}-sessTime-30:qsxglobal999@as.ipidea.io:2334"
}


client = httpx.Client(timeout=_timeout, limits=_limit, follow_redirects=True, proxies=proxy, http2=True, verify=sslgen())
async_client = httpx.AsyncClient(timeout=_timeout, limits=_limit, follow_redirects=True, verify=sslgen(), http2=True)
async_client_proxy = httpx.AsyncClient(timeout=_timeout, limits=_limit, follow_redirects=True, verify=False, http2=True, proxies=proxy_ipidea)


async def batch_rpop(pipeline: pipeline.StrictPipeline, key, n):
    '''
    批量pop
    :param pipeline:
    :param n:
    :param key:
    :return:
    '''
    length = await pipeline.llen(key)
    if length == 0:
        return None
    await pipeline.lrange(key, 0, n - 1)
    await pipeline.ltrim(key, n, -1)
    data = await pipeline.execute()
    return data

def handle_headers(header: dict):
    k_list = []
    _header = deepcopy(header)
    for k in list(header.keys()):
        flag = random.choice([0, 1])
        if k in ["Cache-Control", "Pragma", "sec-ch-ua-mobile", "sec-ch-ua-platform", "sec-fetch-dest", "sec-fetch-mode", "sec-fetch-site", "Proxy-Connection"] and flag == 1:
            _header.pop(k)
        else:
            k_list.append(k)
            continue
    # for i in range(0, 6):
    #     _header[_random_string(random.randint(3, 10))] = _random_string(random.randint(5, 50))
    return _header

def _random_string(length: int) -> str:
    rand_01 = ''
    s = 'qwertyyuiopasdfghjklmnbvcxz0123456789'
    for i in range(length):
        rand_01 += random.choice(s)

    return rand_01

def local2utc(local_tm):
    return datetime.datetime.utcfromtimestamp(local_tm.timestamp() - random.randint(100, 200))


class DataUtil:

    def __init__(self):
        # self.PATH = PATH
        pass

    async def __load_data_into_redis(self, data, name):
        await aio_redis.aredis_db.lpush(f"journals:{name}", data)
        print("journal add success")
    def load_data_into_redis(self, data, name):
        _redis.redis_db.lpush(f"journals:{name}", data)
        print("journal add success")
    @classmethod
    def load_index_data(cls, PATH, name):
        wkbook = openpyxl.load_workbook(PATH)
        wksheet = wkbook.active
        for i in wksheet["A"][0::]:
            cls().load_data_into_redis(i.value, name)

        # tasks = [self.load_data_into_redis(d.value, name) for d in wksheet["A"][1::]]
        # await asyncio.gather(*tasks)