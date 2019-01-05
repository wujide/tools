#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2019/1/5
# @Author: wujide
import os
import shutil


def cmp_files(dir_first, dir_second):
    """
    找出dir_first 中所有的文件，遍历所有的文件 并和 dir_second 中所有的文件名相比较
    找到，则将dir_second 移到 duplicated_files 文件中，并继续查找，直到结束
    :param dir_first:
    :param dir_second:
    :return:
    """
    files_path_list = get_files(dir_first)
    for file_path in files_path_list:
        file = os.path.split(file_path)[1]
        find_duplicated_files(file, dir_second)


# 找出文件夹下所有文件,返回绝对路径+文件名
def get_files(abspath):
    files_path_list = []
    for x in os.listdir(abspath):
        if not x.startswith('.'):
            path = abspath + '/' + x
            if os.path.isfile(path):
                files_path_list.append(path)
            else:
                get_files(path)
    return files_path_list


def find_duplicated_files(file, dir_second):
    files_second_list = get_files(dir_second)
    for x in files_second_list:
        file_sec = os.path.split(x)[1]
        if os.path.isfile(x):
            if file == file_sec:
                print(file_sec, 'is duplicated in :', path)
                print(file_sec, 'is moved to: duplicated_files')
                move_files(x)
                continue
        else:
            # print(file, "comparing in:", path)
            find_duplicated_files(file, x)

    # for x in os.listdir(dir_second):
    #     path = dir_second + '/' + x
    #     if os.path.isfile(path):
    #         if file == x:
    #             print(x, 'is duplicated in :', path)
    #             print(x, 'is moved to: duplicated_files')
    #             move_files(path)
    #             continue
    #     else:
    #         # print(file, "comparing in:", path)
    #         find_duplicated_files(file, path)


def move_files(duplicate_files):
    dup_file_path = '/Users/wujide/Documents/duplicated_files'
    shutil.move(duplicate_files, dup_file_path)


def all_files(file_path):
    # file_path 下面所有的目录或文件列表（不包含隐藏文件）
    paths = [os.path.join(file_path, x)
             for x in os.listdir(file_path) if not x.startswith('.')]
    # 遍历列表，将第i个文件同i+1，+2... 个相比较
    for i in range(len(paths) - 1):
        for path in paths[(i + 1):]:
            # print(paths[i], '<------------->', path)
            cmp_files(paths[i], path)
            # find_duplicated_files(paths[i], path)


if __name__ == '__main__':
    path = '/Users/wujide/Documents/照片备份/'
    all_files(path)
