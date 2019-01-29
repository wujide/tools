#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/12/22
# @Author: wujide
import os
from functools import reduce


'''
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


import sys
import os


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


path = os.path.abspath(os.path.dirname(__file__))
type = sys.getfilesystemencoding()
sys.stdout = Logger('a.txt')

print(path)
print(os.path.dirname(__file__))
print('------------------')
'''