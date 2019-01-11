import hashlib
import os
import random
import shutil
import stat
import sys
import time
from pathlib import Path
from demo.log_redirection import Logger
sys.stdout = Logger('dup_file_log.log')

dup = {}
dir_num = 0
file_num = 0

"""
1. 支持文件名不同但实际是同一文件的去重，暂时只支持jpg，png格式
2. 支持嵌套文件夹的去重
3. 多个相同的文件，会将除第一个文件外的文件移动到指定文件夹（默认值），并改名为原文件名_年月日时分秒_随机值
4. 用户输入需要去重的路径 和 存放重复文件的路径
5. 实测结果：

"""


def move_files(duplicate_files, file_dup_path):
    os.chmod(file_dup_path, stat.S_IWOTH)  # 更改文件属性，使其它用户具有写权限
    return shutil.move(duplicate_files, file_dup_path)


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
def find_dup_files(file_dir, dup_file_dir):
    def get_duplicate():
        return {k: v for k, v in dup.items() if len(v) > 1}

    build_dup_dict(file_dir)
    for hash, files in get_duplicate().items():
        print("重复文件为：", "{}: {}".format(hash, files))
        for file in files[1:]:
            try:
                move_files(file, dup_file_dir)
                print("Moving...")
            except shutil.Error:
                # 如果存在多个重复文件，则重命名后再次移动
                file_split = os.path.split(file)
                file_split_text = os.path.splitext(file)
                file_rename = file_split_text[0] + '_' + time.strftime('%Y%m%d%H%M%S') + '_' + str(random.random()) + file_split_text[1]
                print("遇到多个重复文件，需要重命名再移动：", file_split[1], '======>', os.path.split(file_rename)[1])
                os.renames(file, file_rename)
                move_files(file_rename, dup_file_dir)


def file_stat(dir):
    global dir_num, file_num
    for x in os.listdir(dir):
        path = dir + '/' + x
        if os.path.isdir(path):
            dir_num += 1
            file_stat(path)
        # elif os.path.isfile(path) and not path.endswith(('.DS_Store', '.dat')):  # 如果需要排除文件用这个
        elif os.path.isfile(path):
            file_num += 1
    return dir_num, file_num


if __name__ == '__main__':
    # num = file_stat(PHOTO_PATH)
    # print(PHOTO_PATH, "文件夹下共有：", num[0], "个文件夹和 ", num[1], "个文件")
    # PHOTO_PATH = '/Users/wujide/Documents/照片备份/'
    # DUP_FILE_PATH = '/Users/wujide/Documents/duplicated_files/'
    # file_dir = 'E:\\test_files'
    # file_dup_path = 'E:\\duplicated_files'
    while True:
        file_dir = input("请输入文件路径： ")
        file_dup_path = input("请输入重复文件保存路径： ")
        # if not os.path.exists(file_dup_path):
        #     file_dup_path = file_dup_path or 'C:\\duplicate_files'
        #     os.mkdir(file_dup_path)  # for windows
        num = file_stat(file_dir)
        print(file_dir, "文件夹下共有：", num[0], "个文件夹和 ", num[1], "个文件")
        if input("是否开始扫描Y/N,回车继续：").upper() == 'N':
            print('2秒钟后关闭')
            time.sleep(2)
            break
        find_dup_files(file_dir, file_dup_path)
        if input("是否继续Y/N,回车继续：").upper() == 'N':
            print('3秒钟后关闭, Log 文件保存在当前路径下 dup_file_log.log 中')
            time.sleep(3)
            break
