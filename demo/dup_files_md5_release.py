import hashlib
import os
import random
import shutil
import sys
import time
from pathlib import Path
from demo.log_redirection import Logger
# sys.stdout = Logger('dup_file_log.txt')

dup = {}
dir_num = 0  # 文件夹个数
file_num = 0  # 文件个数
IGNORE_PREFIX_TUP = ('System',)  # 前缀
IGNORE_POSTFIX_TUP = ('.mp4', '.BIN', '.DS_Store')  # 后缀
"""
Notes：
1. 支持文件改名后的去重（使用md5算法）
2. 支持嵌套文件夹的去重
3. 支持mac，windows
4. 多个相同的文件，会将除第一个文件外的文件移动到指定文件夹（用户自己创建并输入），并改名为：原文件名_年月日时分秒_随机值
5. 用户需要输入去重的绝对路径 和 存放重复文件的路径，如对demo 文件夹下的所有的子文件夹和文件去重：d:\demo, d:\demo_bak
6. 为了提高速度，暂时将'.mp4'文件排除，根据需要自行添加或删除前缀，后缀常量：IGNORE_PREFIX_TUP，IGNORE_POSTFIX_TUP；
7. 效率还未优化，实测结果：

"""


# 将 src 文件移入 dest_path 路径下
def move_files(src, dest_path):
    # os.chmod(dest_path, stat.S_IWOTH)  # 更改文件属性，使其它用户具有写权限，windows需要
    return shutil.move(src, dest_path)


# 计算文件的md5
def md5sum(filename, blocksize=65536):
    md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            md5.update(block)
    return md5.hexdigest()


# 建立文件的md5:文件路径的对应关系，多个相同文件则为md5:[文件列表]
def build_dup_dict(dir_path, pattern='*.*'):
    def save(file):
        hash_val = md5sum(file)
        if hash_val not in dup.keys():
            dup[hash_val] = [file]
        else:
            dup[hash_val].append(file)
    p = Path(dir_path)
    for item in p.rglob(pattern):
        if os.path.splitext(item)[1] not in ['.mp4']:
            save(str(item))


# 统计执行时间
def get_time(func):
    def wraper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Spend(seconds):", end_time - start_time)
        return result
    return wraper


# 查找，并移动文件，多个相同的文件，则更改名字移入
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


# 遍历文件夹
def get_listdir(path):
    for f in os.listdir(path):
        if not f.startswith(IGNORE_PREFIX_TUP) and not f.endswith(IGNORE_POSTFIX_TUP):
            yield f


# 统计文件夹与文件个数
def file_stat(dir_src):
    global dir_num, file_num
    for x in get_listdir(dir_src):
        path = dir_src + '/' + x
        if os.path.isdir(path):
            dir_num += 1
            file_stat(path)
        # elif os.path.isfile(path) and not path.endswith(('.DS_Store', '.dat')):  # 如果需要排除文件用这个
        elif os.path.isfile(path):
            file_num += 1
    return dir_num, file_num


if __name__ == '__main__':
    # file_src = '/Users/wujide/Documents/照片备份/'
    # file_dup_path = '/Users/wujide/Documents/duplicated_files/'
    # num = file_stat(file_src)
    # print(file_src, "文件夹下共有：", num[0], "个文件夹和 ", num[1], "个文件")
    # find_dup_files(file_src, file_dup_path)

    # file_dir = 'E:\\test_files'
    # file_dup_path = 'E:\\duplicated_files'
    while True:
        file_src = input("请输入文件路径： ")
        file_dup_path = input("请输入重复文件保存路径： ")
        # if not os.path.exists(file_dup_path):
        #     file_dup_path = file_dup_path or 'duplicate_files'
        #     os.mkdir(file_dup_path)  # for windows
        num = file_stat(file_src)
        print(file_src, "文件夹下共有：", num[0], "个文件夹和 ", num[1], "个文件")
        if input("是否开始扫描Y/N,回车继续：").upper() == 'N':
            print('2秒钟后关闭')
            time.sleep(2)
            break
        print("扫描中......请稍候")
        find_dup_files(file_src, file_dup_path)
        if input("是否继续Y/N,回车继续：").upper() == 'N':
            print('3秒钟后关闭...')
            # print('3秒钟后关闭, Log 文件保存在当前路径下 dup_file_log.txt 中')
            time.sleep(3)
            break

