# -*- conding:utf-8 -*-
#公共代码
import os
from conf import settings
import hashlib
import logging.config

#判断是否已经登录
from core import src
def login_auth(func):
    def inner(*args,**kwargs):
        if src.user_info['user']:
            res = func(*args,**kwargs)
            return res
        else:
            print('请去登录')
    return inner


#hashlib加密
def get_md5(pwd):
    val = '天王盖地虎'
    md5 = hashlib.md5()  #创建一个md5对象
    # md5.update(pwd)  #传进来的参数加密
    md5.update(pwd.encode('utf-8'))
    md5.update(val.encode('utf-8'))  #加盐操作
    res = md5.hexdigest()
    return res

# 日志功能
def get_logger(type_name):
    logging.config.dictConfig(settings.LOGGING_DIC)
    logger = logging.getLogger(type_name)
    return logger







