#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time: 2018/10/29
# @Author: wujide

import time


def get_time(func):
    def wraper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print("Spend:", end_time - start_time)
        return result
    return wraper


@get_time
def _list(n):
    l1 = [list(range(n)) for i in range(n)]
    del l1


@get_time
def _generator(n):
    ge = (tuple(range(n)) for i in range(n))
    del ge



_list(10000)
_generator(10000)