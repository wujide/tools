#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2019/1/29
# @Author: wujd

import redis
from readConfig import ReadConfig


class RedisManager:
    def __init__(self, db_num):
        local_config = ReadConfig()
        host = local_config.get_redis('host')
        password = local_config.get_redis('password')
        # 使用connection pool来管理对一个redis server的所有连接，避免每次建立、释放连接的开销。
        # 默认，每个Redis实例都会维护一个自己的连接池。可以直接建立一个连接池，然后作为参数Redis，这样就可以实现多个Redis实例共享一个连接池。
        pool = redis.ConnectionPool(host=host, password=password, db=db_num, decode_responses=True)
        self.r = redis.Redis(connection_pool=pool)

    def get_name_hash(self, name, key):
        return self.r.hget(name, key)

    # 获取name对应hash的所有键值
    def get_name_hash_all(self, name):
        return self.r.hgetall(name)

    def get_name_string(self, name):
        return self.r.get(name)

    def get_list_len(self, name):
        return self.r.llen(name)

    def get_list_item(self, name, start, end):
        return self.r.lrange(name, start, end)

    def set_name_hash(self, name, value):
        return self.r.set(name, value)

    # todo: 如何实现修改name下面单个key的值 ？
    def set_name_string(self, name, value):
        return self.r.set(name, value)

    # 经测试，可用于hash, string, list
    def del_name(self, name):
        self.r.delete(name)

    def del_name_hash(self, name, key):
        self.r.hdel(name, key)

# list
rd = RedisManager(db_num=3)
# v_list = rd.get_list_len('activity:carve_up:bonus_pool')
v_list = rd.get_list_item('activity:carve_up:bonus_pool', 0, -1)
print(len(v_list))
print(v_list.count('1'))
print(v_list.count('2'))
print(v_list.count('3'))
print(v_list.count('4'))
# print(v_list)



'''
# hash
rd = RedisManager(db_num=15)
# redis-py默认在执行每次请求都会创建（连接池申请连接）和断开（归还连接池）一次连接操作，
# 如果想要在一次请求中指定多个命令，则可以使用pipline实现一次请求指定多个命令，并且默认情况下一次pipline 是原子性操作。
pipe = r.pipeline(transaction=True)

v = rd.get_name_hash('test_set')
print(v)
v_all = rd.get_name_hash_all('123456')
print(v_all)

pipe.execute()

rd = RedisManager(db_num=2)
v = rd.get_name_hash('offline:promot_user_key:401115537', 'coin_total')
print(v)
v_all = rd.get_name_hash_all('offline:promot_user_key:401115537')
print(v_all)
'''

'''
# string
rd = RedisManager(db_num=15)
v_string = rd.get_name_string('task_conf_hot')
print(v_string)
v_modify = [
  {
    "id": "13",
    "task_name": "应用授权",
    "task_icon": "\/xingqiuimg\/upload\/201807\/task\/task_icon_153267017817.png",
    "task_pic_1": "",
    "task_pic": "",
    "task_desc": "根据引导开启权限即可",
    "task_value": "100",
    "value_display_unit": "2",
    "task_button": "去授权",
    "task_installed_desc": "",
    "task_uninstalled_desc": "",
    "task_label": "",
    "task_url": "",
    "task_status": "1",
    "task_first_open": "",
    "task_open": "",
    "sub_task_rule": "",
    "task_detail": "",
    "task_tag": "xq_authorization",
    "task_type": "1",
    "task_month_get": "0.00",
    "task_day_get": "",
    "task_app_size": "",
    "task_app_desc": "",
    "task_app_popup": "",
    "task_app_min_version": "",
    "is_remind_upgrade": "0",
    "remind_upgrade_version": "",
    "remind_upgrade_text": "",
    "task_app_deeplink": "",
    "download_url": "",
    "package_name": "",
    "hide_channel": "[]",
    "app_version": "3.2",
    "recommend_sub_task": "0",
    "sub_corner_icon": "",
    "sub_button_type": "0",
    "ctime": "2018-07-27 13:42:58",
    "mtime": "2019-01-02 14:32:36"
  }]
# v_string_set = rd.set_name_string('task_conf_hot', str(v_modify))
# print(rd.get_name_string('task_conf_hot'))

rd.del_name('list:task:init_redo')
# rd.del_name_hash('123456', 'attr_2')
'''
