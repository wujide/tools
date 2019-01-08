import hashlib
import os
import shutil
import time
from pathlib import Path

dup = {}
PHOTO_PATH = '/Users/wujide/Documents/照片备份/'
DUP_FILE_PATH = '/Users/wujide/Documents/duplicated_files/'


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


def main():
    def get_duplicate():
        return {k: v for k, v in dup.items() if len(v) > 1}

    build_dup_dict(PHOTO_PATH)
    for hash, files in get_duplicate().items():
        print("{}: {}".format(hash, files))
        print("moving file===: ", files[1], "==> to [dup_file_path]")
        for file in files[1:]:
            try:
                move_files(file)
            except shutil.Error:
                print("Destination path(files) already exists!")
                print("rename the exists files: ", file)
                file_rename = file + time.strftime('%Y%m%d %H%M%S')
                os.renames(file, file_rename)
                move_files(file_rename)


if __name__ == '__main__':
    main()
