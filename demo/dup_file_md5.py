import hashlib
import os
import shutil
import time
from pathlib import Path

dup = {}
# PHOTO_PATH = '/Users/wujide/Documents/照片备份/'
# DUP_FILE_PATH = '/Users/wujide/Documents/duplicated_files/'
PHOTO_PATH = 'E:\\test_files'
DUP_FILE_PATH = 'E:\\duplicated_files'

"""
1. 支持文件名不同但实际是同一文件的去重
2. 支持嵌套文件夹的去重
3. 多个相同的文件，会将除第一个文件外的文件移动到指定文件夹（默认值），并改名为原文件名 + 年月日时分秒

"""
# todo: 加上用时统计
# todo: 加上log记录到文件


def move_files(duplicate_files):
    return shutil.move(duplicate_files, DUP_FILE_PATH)


def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


def build_dup_dict(dir_path, pattern='*.jpg'):
    def save(file):
        hash = md5sum(file)
        if hash not in dup.keys():
            dup[hash] = [file]
        else:
            dup[hash].append(file)

    p = Path(dir_path)
    for item in p.rglob( pattern):
        save(str(item))


def find_dup_files():
    def get_duplicate():
        return {k: v for k, v in dup.items() if len(v) > 1}

    build_dup_dict(PHOTO_PATH)
    for hash, files in get_duplicate().items():
        print("重复文件为：", "{}: {}".format(hash, files))
        print("Moving file===: ", files[1], "==> ", DUP_FILE_PATH)
        for file in files[1:]:
            try:
                move_files(file)
            except shutil.Error:
                # 如果存在多个相同文件，则重命名后再次移动
                print("Destination path(files) already exists!")
                file_rename = file + time.strftime('%Y%m%d%H%M%S')
                print("rename：", file, '======>', file_rename)
                os.renames(file, file_rename)
                move_files(file_rename)


if __name__ == '__main__':
    find_dup_files()
