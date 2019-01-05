#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/12/22
# @Author: wujide
import os


def search_file(abspath, str):
    for x in os.listdir(abspath):
        # print(str, x)
        if os.path.isfile(abspath+'/'+x):
            if str == x:
                print(x, 'path is', abspath)
                break
            # else:
            #     print(x, 'is not the file')
        else:
            search_file(abspath + '/' + x, str)


path = '/Users/wujide/Documents/python_project/tools/'
# print(os.listdir(os.path.abspath(path)))
# print(os.path.abspath(path))
search_file(os.path.abspath(path), 'yyx.log')
