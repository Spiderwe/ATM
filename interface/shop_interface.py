# -*- conding:utf-8 -*-
from db import db_handler
from interface import bank_interface
from lib import common
#日志
shop_logger = common.get_logger('shop')

#用户购买接口
def buy_shop_interface(user,count):
    flag = bank_interface.shop_money_interface(user,count)  #银行消费支付接口
    if flag:
        shop_logger.info('购物成功')
        return True,'购物成功'
    else:
        shop_logger.info('余额不足，购物失败')
        return False,'余额不足，购物失败'

#添加购物车接口
def add_shop_car_interface(user,shop_car):
    user_dic = db_handler.select(user)

    #用户原始的购物车信息表
    old_shop_car = user_dic['shop_cart']

    #循环取出购物车里面的商品(取出商品名)，用来判断原始的购物车里面是否存在
    for shop in shop_car:
        if shop in old_shop_car:
            #获取当前购物车的商品数量
            num = shop_car[shop]
            #如果购物车里面已经存在的商品就直接加上数量就可以了
            old_shop_car[shop] += num
        else:
            # 获取当前购物车的商品数量
            num = shop_car[shop]
            #如果原始购物车没有这个商品，那么就直接是这个数量
            old_shop_car[shop] = num

    #利用字典的update方法，有key就修改值，没有key就添加一个新的键值对
    user_dic['shop_cart'].update(old_shop_car)
    db_handler.save(user_dic)
    shop_logger.info('添加购物车成功')
    return True,'添加购物车成功'


#查看购物车接口
def check_shop_car_interface(user):
    user_dic = db_handler.select(user)
    return user_dic['shop_cart']
