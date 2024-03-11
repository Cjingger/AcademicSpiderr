# -*- encoding: utf-8 -*-
import datetime
import json
import os
from common.Files import Files
import aredis, asyncio

# path = r"E:\project\new_scopus"
ylFile = Files()
redis_items = ylFile.getConfigDict("Redis-Config-ali")
REDIS_HOST = redis_items['host']
REDIS_DB = redis_items['db']
REDIS_PORT = redis_items['port']
REDIS_PASSWORD = redis_items['code']


class AioRedisUtil(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB):
        self.pool = aredis.ConnectionPool()
        self.aredis_db = aredis.StrictRedis(host=host, port=port, password=password, db=db, max_connections=2 ** 20, connect_timeout=30)
        # , connection_pool=self.pool)

    async def back_in_redis(self, name, data):
        await self.aredis_db.rpush(name, data)



async def get_proxies(now_time):
    '''
    获取代理
    :return:
    '''
    proxy_list = []
    try:
        aredis_db_poxy = AioRedisUtil(db=7)
        proxies = await aredis_db_poxy.aredis_db.get("proxies")
        __proxies: list = eval(bytes.decode(proxies))
        for p in __proxies:
            proxy, overdue_time = str(p).split("----")[0], str(p).split("----")[1]
            overdue_time = datetime.datetime.strptime(overdue_time, "%Y-%m-%d %H:%M:%S")
            # 代理已过期,抛掉
            if overdue_time < now_time:
                pass
            else:
                proxy_list.append(proxy)
        # print("proxies", proxy_list)
        return proxy_list
    except:
        return proxy_list


async def get_refreshed_token():
    '''

    :return:
    '''
    aredis_db = AioRedisUtil(db=1)
    success, fail = 0, 0
    all_keys = await aredis_db.aredis_db.hgetall("check")
    # print("all_token_data", all_token_data)
    for key in all_keys:
        key = bytes.decode(key)
        token_data = await aredis_db.aredis_db.hget("check", key)
        token_data = eval(bytes.decode(token_data))
        # print("token_data", token_data)
        if has_key(token_data, "successTime") and has_key(token_data, "isRefresh"):
            if token_data['isRefresh'] == 1:
                success += 1
            else:
                fail += 1
        else:
            fail += 1
    print(f"rate: {round(success / success + fail, 4)}")


async def get_fingerprint():
    aredis_db = AioRedisUtil(db=0)
    all_data = await aredis_db.aredis_db.lrange("px:fingerprint:test20221228:user:list", 0, -1)
    l1 = []; l2 = []; l3 = []
    for d in all_data:
        d = json.loads(bytes.decode(d))
        # if d["user-agent"] == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36":
        #     l1.append(d)
        # elif d["user-agent"] == "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36":
        #     l2.append(d)
        # elif d["user-agent"] == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54":
        #     l3.append(d)
        if d["user-agent"] == "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36":
            print(d)
            break

def has_key(obj: dict, key_name: str):
    try:
        if obj.get(key_name) is not None:
            return True
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    for i in range(10):
    # asyncio.get_event_loop().run_until_complete(get_proxies())
        asyncio.get_event_loop().run_until_complete(get_fingerprint())
