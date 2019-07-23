# -*- conding:utf-8 -*-
#用户信息的接口层
from conf import  settings
import json
from db import db_handler
from lib import common

user_logger = common.get_logger('user')
#用户注册接口
def register_interface(username,password,balance=15000):
    #加密处理
    password = common.get_md5(password)
    user_dict = {
        'user': username,
        'pwd': password,
        'balance': balance,
        'flow': [],
        'shop_cart': {},
        'lock': False  #冻结账户
    }
    #保存注册用户的信息
    db_handler.save(user_dict)
    user_logger.info('%s用户注册成功'%user_dict['user'])
    return True

#查看用户接口
def register_interface_select(username):
    user_dict = db_handler.select(username)
    if user_dict:
        return True

#用户登录查询接口
def login_interface(username,pwd):
    #获取用户登录输入的密码加密后的结果
    pwd = common.get_md5(pwd)
    #获取用户注册的加密密码
    user_dic = db_handler.select(username)

    if user_dic['lock'] == True:
        user_logger.info('%s用户已经被冻结，请联系管理员'%username)
        return False,'%s用户已经被冻结，请联系管理员'%username

    if pwd == user_dic['pwd']:
        user_logger.info('%s用户登录成功'%username)
        return True,'登录成功'
    else:
        user_logger.info('输入信息不正确,请重新输入')
        return False,'输入信息不正确,请重新输入'


#用户注销接口
def logout_interface():
    from core import src
    user = src.user_info['user']
    src.user_info['user'] = None
    user_logger.info('%s用户已经注销'%user)
    return '%s用户已经注销'%user


#冻结用户接口
def lock_user_interface(user):
    user_dic = db_handler.select(user)
    user_dic['lock'] = True
    db_handler.save(user_dic)
    user_logger.info('%s用户冻结成功'%user)
    return True,'%s用户冻结成功'%user

#解冻用户
def unlock_user_interface(user):
    user_dic = db_handler.select(user)
    user_dic['lock'] = False
    db_handler.save(user_dic)
    user_logger.info('%s用户解冻成功' % user)
    return True, '%s用户解冻成功' % user

#修改额度接口
def change_limit_interface(user,change_limit_money):
    user_dic = db_handler.select(user)
    user_dic['balance'] = change_limit_money
    msg = '%s用户修改额度为%s'%(user,change_limit_money)
    user_dic['flow'].append(msg)
    db_handler.save(user_dic)
    user_logger.info('%s用户修改额度为%s'%(user,change_limit_money))
    return True,msg