import hashlib
import os
import random
import shutil
import time
from pathlib import Path
# from decorator_time import get_time

dup = {}
# PHOTO_PATH = '/Users/wujide/Documents/照片备份/'
# DUP_FILE_PATH = '/Users/wujide/Documents/duplicated_files/'
PHOTO_PATH = 'E:\\test_files'
DUP_FILE_PATH = 'E:\\duplicated_files'

"""
1. 支持文件名不同但实际是同一文件的去重，暂时只支持jpg，png格式
2. 支持嵌套文件夹的去重
3. 多个相同的文件，会将除第一个文件外的文件移动到指定文件夹（默认值），并改名为原文件名_年月日时分秒_随机值
4. 用户输入需要去重的路径 和 存放重复文件的路径
5. 实测结果：

"""


def move_files(duplicate_files):
    return shutil.move(duplicate_files, DUP_FILE_PATH)


def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def build_dup_dict(dir_path, pattern='*.*'):
    def save(file):
        hash = md5sum(file)
        if hash not in dup.keys():
            dup[hash] = [file]
        else:
            dup[hash].append(file)

    p = Path(dir_path)
    for item in p.rglob(pattern):
        save(str(item))


def get_time(func):
    def wraper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Spend(seconds):", end_time - start_time)
        return result
    return wraper


@get_time
def find_dup_files():
    def get_duplicate():
        return {k: v for k, v in dup.items() if len(v) > 1}

    build_dup_dict(PHOTO_PATH)
    for hash, files in get_duplicate().items():
        print("重复文件为：", "{}: {}".format(hash, files))
        for file in files[1:]:
            try:
                move_files(file)
                print("Moving...")
            except shutil.Error:
                # 如果存在多个重复文件，则重命名后再次移动
                file_split = os.path.split(file)
                file_split_text = os.path.splitext(file)
                file_rename = file_split_text[0] + '_' + time.strftime('%Y%m%d%H%M%S') + '_' + str(random.random()) + file_split_text[1]
                print("遇到多个重复文件，需要重命名再移动：", file_split[1], '======>', os.path.split(file_rename)[1])
                os.renames(file, file_rename)
                move_files(file_rename)


def file_stat(file_dir):
    p = Path(file_dir)
    ps = p.rglob('*.*')


if __name__ == '__main__':
    # todo: 加入对输入文件夹下子文件夹，文件个数的统计
    # todo: 加入对用户输入路径的判断，不存在则创建
    while True:
        FILE_PATH = input("请输入文件路径： ")
        FILE_DUP_PATH = input("请输入重复文件保存路径： ")
        find_dup_files()
