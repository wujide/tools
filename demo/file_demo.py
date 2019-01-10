#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/11/3
# @Author: wujide
import os
import os.path

dir_num = 0
file_num = 0


def file_stat(file_dir):
    global dir_num, file_num
    for x in os.listdir(file_dir):
        path = file_dir + '/' + x
        # print(file_dir)
        if os.path.isdir(path):
            dir_num += 1
            file_stat(path)
        # elif os.path.isfile(path) and not path.endswith(('.DS_Store', '.jpg')):
        elif os.path.isfile(path):
            file_num += 1
    # print(file_dir, "文件夹下共有：", dir_num, "个文件夹和 ", file_num, "个文件")
    return dir_num, file_num


data = file_stat("/Users/wujide/Documents/照片备份/")
print(data)

# file_stat("/Users/wujide/Documents/照片备份/20130621-Birthday/")
# file_stat("/Users/wujide/Documents/照片备份/20130621-Birthday/")
(22, 4258)