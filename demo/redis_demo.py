#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2019/1/29
# @Author: wujd

import redis
from readConfig import ReadConfig

# local_config = ReadConfig()
# host = local_config.get_redis('host')
# password = local_config.get_redis('password')
# db2 = local_config.get_redis('db')


class RedisManager:
    def __init__(self, db_num):
        local_config = ReadConfig()
        host = local_config.get_redis('host')
        password = local_config.get_redis('password')
        pool = redis.ConnectionPool(host=host, password=password, db=db_num, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    def get_name(self, name):
        return self.r.get(name)

    # 获取name对应hash的所有键值
    def get_name_all(self, name):
        return self.r.hgetall(name)

    def set_name(self, name, value):
        return self.r.set(name, value)

    def del_name(self, name):
        self.r.delete(name)


rd = RedisManager(db_num=15)
v = rd.get_name('test_set')
print(v)
v_all = rd.get_name_all('123456')
print(v_all)

# pool = redis.ConnectionPool(host=host, password=password, db=db2, decode_responses=True)
# r = redis.Redis(connection_pool=pool)
# print(r.dbsize())
# print(r.hget('offline:promot_user_key:401115537', 'coin_total'))
# val_all = r.hgetall('offline:promot_user_key:401115537')
# print(val_all)

'''
pool = redis.ConnectionPool(host=host, password=password, db=15, decode_responses=True)
r = redis.Redis(connection_pool=pool)
print(r.dbsize())
# 增
r.set('test', 1)
print(r.get('test'))

# 删
print(r.get('test'))
r.delete('test')
print(r.get('test'))

# 改
a = r.get('test_set')
print(a)
r.set('test_set', int(a)+1)
print(r.get('test_set'))


r.hset("123456", "attr_1", 100)
print(r.hget("123456", "attr_1"))

'''

