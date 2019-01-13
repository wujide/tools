#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2019/1/11
# @Author: wujd

import sys
import os
from time import sleep


class Logger(object):
    def __init__(self, filename="Default.log"):
        self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass


def log_to_file(msg):
    temp = sys.stdout
    with open('dup_file_log.txt', 'a+') as f:
        sys.stdout = f
        print(msg)
    sys.stdout = temp
    print(456)


if __name__ == '__main__':
    sleep(2)
    log_to_file('123')
    sleep(2)
    print('789')
    sleep(2)

