#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2019/3/8
# @Author: wujd

import hashlib


# 读取文件得到list，并去掉item后面的 '\n'
def read_uid():
    with open('demo/config/user_1.txt', 'r') as f:
        uid_list = f.readlines()
    for i in range(0, len(uid_list)):
        uid_list[i] = uid_list[i].strip('\n')
    return uid_list


def uid_2_md5():
    uid_list = read_uid()
    uid_list_md5 = []
    for uid in uid_list:
        md_val = hashlib.md5(uid.encode()).hexdigest()
        print(uid, "---->", md_val)
        uid_list_md5.append(md_val)
    with open('user_1_md5.txt', 'a') as f:
        for md_val in uid_list_md5:
            f.write(md_val)
            f.write('\n')


if __name__ == '__main__':
    uid_2_md5()
