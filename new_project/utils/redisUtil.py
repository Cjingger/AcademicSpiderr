# -*- encoding: utf-8 -*-
import os
import random
import redis
from common.Files import Files

path = r"E:\project\new_scopus"
# ylFile = Files(os.path.abspath('.'))
ylFile = Files()
redis_items = ylFile.getConfigDict("Redis-Config-ali")
REDIS_HOST = redis_items['host']
REDIS_DB = redis_items['db']
REDIS_PORT = redis_items['port']
REDIS_PASSWORD = redis_items['code']


class RedisUtil(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB):
        self.conn_pool = redis.ConnectionPool(host=host, port=port, max_connections=2 ** 10, password=password, db=db)
        self.redis_db = redis.Redis(connection_pool=self.conn_pool, socket_timeout=6, socket_connect_timeout=5, retry_on_timeout=True, retry_on_error=True, retry=2)

    def set(self, name, username, value):
        '''

        :param username: 用户名
        :param value: cookie
        :return:
        '''

        return self.redis_db.hset(name, username, value)

    def get(self, name, username):
        '''
        根据键名获取键值
        :param username:
        :return:
        '''
        return self.redis_db.hget(name, username)

    def delete(self, name, username):
        '''
        根据键名删除键值对
        :param username:
        :return:
        '''
        return self.redis_db.hdel(name, username)

    def cout(self, name):
        '''
        获取数目
        :return:
        '''
        return self.redis_db.hlen(name)

    def random(self, name):
        '''
        随机获取cookie
        :return:
        '''
        return random.choice(self.redis_db.hvals(name))

    def usernames(self, name):
        '''
        获取所有账号信息
        :return:
        '''
        return self.redis_db.hkeys(name)

    def values(self, name):
        '''
        获取所有键值对
        :return:
        '''
        return self.redis_db.hgetall(name)

    def sset(self, name, value):
        '''
        设置set值
        :return:
        '''
        self.redis_db.sadd(name, value)

    def sget(self, name, count):
        '''
        从set取出值
        :param name: set名
        :param count: 取出的个数
        :return:
        '''
        return self.redis_db.spop(name, count)

    def exist_key(self, name):
        if self.redis_db.exists(name) == 1:
            return True
        elif self.redis_db.exists(name) == 0:
            return False
        else:
            raise ConnectionError

    def hash_exist_key(self, name, key):
        if self.redis_db.hexists(name, key):
            return True
        else:
            return False

    def set_expire(self, name, time: int):
        self.redis_db.expire(name, time)

    def sremove(self, name):
        num = self.redis_db.scard(name)
        self.redis_db.spop(name, num)

    def sranmember(self, name):
        return str(self.redis_db.srandmember(name, 1)[0], encoding='utf-8')

    def close(self):
        self.redis_db.close()
