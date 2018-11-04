#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/11/4
# @Author: wujide

"""
json 学习
json.dumps()    返回一个str，内容就是标准的JSON
json.loads()    把JSON的字符串反序列化

json.dump()     直接把JSON写入一个file-like Object
json.load()     从file-like Object中读取字符串并反序列化
"""
import json
import logging
logging.basicConfig(level=logging.INFO)


class Student(object):
    def __init__(self, name, age, score):
        self.name = name
        self.age = age
        self.score = score


def student2dict(std):
    return {
        'name': std.name,
        'age': std.age,
        'score': std.score
    }


# 可选参数default就是把任意一个对象变成一个可序列为JSON的对象，我们只需要为Student专门写一个转换函数，再把函数传进去即可：
s = Student('Bob', 20, 88)
print(json.dumps(s, default=student2dict))
print(json.dumps(s, default=lambda obj: obj.__dict__))


def dict2student(d):
    return Student(d['name'], d['age'], d['score'])


json_str = '{"age": 20, "score": 88, "name": "Bob"}'
print(json.loads(json_str, object_hook=dict2student))   # 反序列化的Student实例对象
