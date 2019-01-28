#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
功能：
    登录验证模块
详细说明：
    1.密码文件为passwd
    2.passwd未创建或丢失，会提示：密码文件不存在，建议重新注册！！
    3.未注册用户登录会提示：用户名不存在，请您先进行注册！
    4.已注册用户登录时，忘记密码，尝试3次后密码还不正确则退出验证，等一会儿则可以重新登录
    5.作为装饰器进行登录验证
"""
import json
import hashlib
import os
pwd = os.getcwd()
fileName = os.path.join(pwd, "passwd")

# 将明文密码通过md5进行加密,返回一个加密后的md5的值


def calc_md5(passwd):
    md5 = hashlib.md5("haliluya".encode('utf-8'))
    md5.update(passwd.encode('utf-8'))
    ret = md5.hexdigest()
    return ret


# 新用户注册模块
def register():
    # 判断密码文件passwd是否存在，存在则载入列表，不存在就重新创建一个空字典
    if os.path.exists(fileName):
        # 载入用户列表，数据结构为字典，k=userName,v=passwdMd5
        with open("passwd", "r+") as loadsFn:
            userDB = json.loads(loadsFn.read())
    else:
        userDB = {}
    # 让用户输入用户名
    userName = input("姓名：")
    # 标志位：控制循环跳出
    flag = True
    while flag:
        # 用户注册时，需输入两次密码
        passwd1 = input("密码：")
        passwd2 = input("确认密码：")
        # 如果两次密码不一致，则不执行下一步，再次输入密码并进行确认
        if not passwd1 == passwd2:
            continue
        else:
            # 两次输入密码一致，标志位置为False，下次跳出循环
            flag = False
        # 调用calc_md5函数将明文密码转为对应的md5值，用于保存
        passwdMd5 = calc_md5(passwd1)
    # 将用户名与密码对应存入字典userDB中
    userDB[userName] = passwdMd5
    # 将用户名和密码存入文件
    with open(fileName, "w") as dumpFn:
        dumpFn.write(json.dumps(userDB))


# 用户登录验证,装饰器
def login(func):
    def decorater(*args, **kwargs):
        # 判断passwd文件是否存在，存在则载入userDB（用户：密码），否则就重新注册新的passwd文件并返回
        if os.path.exists(fileName):
            with open("passwd", "r+") as loadsFn:
                userDB = json.loads(loadsFn.read())  # todo: AttributeError: module 'json' has no attribute 'loads'
        else:
            print("密码文件不存在，建议重新注册！！")
            register()
            return

        name = input("用户名：")
        # 用户名是否存在，存在就继续输入密码，不存在则进行注册
        if name in userDB.keys():
            flag = True
            counter = 0
            # 循环输入密码，密码正确，flag=False（下次直接跳出循环）并执行函数，密码错误则允许尝试3次，超过3次验证失败，退出验证
            while flag:
                passwd = input("密码：")
                passwdMd5 = calc_md5(passwd)
                if passwdMd5 == userDB[name]:
                    flag = False
                    func(*args, **kwargs)
                elif counter > 2:
                    print("您已经尝试了3次，请过会儿再试！！")
                    return
                else:
                    counter += 1
        else:
            print("用户名不存在，请您先进行注册！")
            register()
    return decorater


if __name__ == "__main__":
    @login
    def hello():
        print("Hello world!")
    hello()
