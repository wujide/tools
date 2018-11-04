#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/11/3
# @Author: wujide

"""

练习：编写一个search(s)的函数，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出完整路径：

$ python search.py test
unit_test.log
py/test.py
py/test_os.py
my/logs/unit-test-result.txt

"""
import os

curPath = os.path.abspath(".")
aimPath = os.path.join(curPath, "selfPath")
keyStr = '_1'

'检索目录及下级目录的文件名是否含有特定字符'


def search(aimPath, keyStr):
    for dir in os.listdir(aimPath):
        factDir = os.path.join(aimPath, dir)
        if os.path.isdir(factDir):
            search(factDir, keyStr)
        elif os.path.isfile(factDir):  # 读取到的是文件
            fileName = os.path.split(factDir)  # 取得文件名
            if fileName[1].find(keyStr) > 0:
                print u"在%s找到了文件%s" % (fileName[0], fileName[1])


search(aimPath, keyStr)
