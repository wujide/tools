#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2019/1/11
# @Author: wujd

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
