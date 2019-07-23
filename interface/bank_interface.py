# -*- conding:utf-8 -*-
#查看余额接口
from db import db_handler
from lib import common
#日志
bank_logger = common.get_logger('bank')

#查询用户余额
def check_bal_interface(username):
    user_dict = db_handler.select(username)
    return user_dict['balance']

#提现接口
def withdraw_interface(money,username):
    #查询到用户的信息
    user_dict = db_handler.select(username)

    money = int(money)
    # 判断余额是否够取出，需要5%的手续费
    if user_dict['balance'] >= money*1.05:
        user_dict['balance'] -= money*1.05
        msg = '%s用户提现金额%s元'%(username,money)
        #用户流水信息
        user_dict['flow'].append(msg)
        db_handler.save(user_dict)
        bank_logger.info('%s用户提现金额%s元'%(username,money))
        return True,msg
    else:
        bank_logger.info('余额不足')
        return False,'余额不足'

#还款接口
def repay_interface(money,username):
    # 查询到用户的信息
    user_dict = db_handler.select(username)
    money = int(money)
    user_dict['balance'] +=money
    msg = '%s用户还款了%s元' %(username,money)
    user_dict['flow'].append(msg)
    #保存数据
    db_handler.save(user_dict)
    bank_logger.info('%s用户还款了%s元' %(username,money))
    return True, msg

#转账接口
def transfer_interface(to_user,from_user,money):
    #查询转账对象
    to_user_dict = db_handler.select(to_user)
    from_user_dict = db_handler.select(from_user)
    money = int(money)

    if from_user_dict['balance'] >= money:  #余额大于转账才可以转钱
        to_user_dict['balance'] += money
        from_user_dict['balance'] -= money

        to_user_msg = '%s用户收到%s用户转账%s元' %(to_user,from_user,money)
        from_user_msg = '%s用户转账给%s用户%s元' %(from_user,to_user,money)

        #添加流水信息
        to_user_dict['flow'].append(to_user_msg)
        from_user_dict['flow'].append(from_user_msg)
        #保存信息
        db_handler.save(to_user_dict)
        db_handler.save(from_user_dict)
        bank_logger.info('%s用户转账给%s用户%s元' %(from_user,to_user,money))
        return True,'转账成功'

    else:
        bank_logger.info('余额不够转账')
        return False,'余额不够转账'


#查看流水接口
def check_flow_interface(username):
    user_dict = db_handler.select(username)
    return user_dict['flow']

#获取用户余额
def check_blance_interface(user):
    user_dict = db_handler.select(user)
    return user_dict['balance']

#银行消费支付接口
def shop_money_interface(user,count):
    user_dict = db_handler.select(user)
    #消费扣款
    if user_dict['balance'] >= count:
        user_dict['balance'] -=count

        msg = '%s用户消费了%s元' %(user,count)
        user_dict['flow'].append(msg)
        db_handler.save(user_dict)
        bank_logger.info('%s用户消费了%s元' %(user,count))
        return True
    else:
        bank_logger.info('余额不足')
        return False