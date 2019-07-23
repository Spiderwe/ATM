# -*- conding:utf-8 -*-
#核心文件代码
from lib import common
from conf import  settings
import json
from interface import user_interface
from interface import bank_interface
from interface import shop_interface
user_info = {
    'user':None
}

#注册
def register():
    print('注册...')
    while True:
        username = input('请输入用户名:').strip()
        #查询用户名是否已经注册
        user_dict = user_interface.register_interface_select(username)
        if user_dict:   #接受返回值，user_dict  存在就是已经注册过了
            print('用户名已经注册了，请重新输入')
            continue

        password = input('请输入密码:').strip()
        conf_pwd = input('请再次输入密码:').strip()
        if password == conf_pwd:
            #使用接口的方式来注册
            flag = user_interface.register_interface(username, password)   #接收返回值
            if flag:
                print('注册成功')
                break
            else:
                print('注册失败')
        else:
            print('两次密码输入不一样，请重新输入')


            #平常的方式
            # user_info = {
            #     'name':username,'pwd':password,'flow':[],'shopping_car':{}
            # }
            # #数据库路径
            # DB_PATH = settings.DB_PATH
            # # 把注册信息写入文件
            # with open(r'%s\%s.json'%(DB_PATH,username),'w',encoding='utf-8') as f:
            #     res = json.dumps(user_info)
            #     f.write(res)
            #     f.flush()
            # print('恭喜你注册成功')
            # break

#登录
def login():
    while True:
        username = input('请输入用户名:').strip()
        flag = user_interface.register_interface_select(username)
        if not flag:
            print('该用户名尚未注册')
            continue

        pwd = input('请输入密码:').strip()
        flag,msg = user_interface.login_interface(username,pwd)
        if flag:
            #登录后做个记录
            user_info['user'] = username
            print(msg)
            break
        else:
            print(msg)

#查看余额
@common.login_auth
def check_bal():
    #通过登录时候保存的用户名来查询余额
    user_balance = bank_interface.check_bal_interface(user_info['user'])
    print(user_balance)

#提现   收取5%的费用
@common.login_auth
def withdraw():
    while True:
        money = input('请输入你需要提现的金额:').strip()
        #判断输入是否为数字
        if not money.isdigit():
            print('请输入数字')
            continue

        flag,msg = bank_interface.withdraw_interface(money,user_info['user'])
        if flag:
            print(msg)
            break
        else:
            print(msg)

#还款  需要输入金额
@common.login_auth
def repay():
    while True:
        money = input('请输入你需要还款的金额:').strip()
        #判断输入是否为数字
        if not money.isdigit():
            print('请输入数字')
            continue
        flag,msg = bank_interface.repay_interface(money,user_info['user'])
        if flag:
            print(msg)
            break

#转账  需要三个参数：转给哪个用户，当前用户，金额
@common.login_auth
def transfer():
    while True:
        to_user = input('请输入要转账的用户:').strip()
        flag = user_interface.register_interface_select(to_user)
        if not flag:
            print('转账的用户不存在')
            continue
        money = input('请输入转账的金额:').strip()
        # 判断输入是否为数字
        if not money.isdigit():
            print('请输入数字')
            continue
        flag,msg = bank_interface.transfer_interface(to_user,user_info['user'],money)
        if flag:
            print(msg)
            break
        else:
            print(msg)


#查看流水
@common.login_auth
def check_flow():
    flows = bank_interface.check_flow_interface(user_info['user'])
    for flow in flows:
        print(flow)


#购物功能
@common.login_auth
def shopping():
    goods_list = [
        ['凤爪', 50],
        ['T-shirt', 150],
        ['macbook', 5000],
        ['iphoneX', 3000]
    ]
    #获取用户的余额
    user_balance = bank_interface.check_blance_interface(user_info['user'])
    #购物车
    shop_car = {}
    #初始总额
    count = 0
    while True:
        #打印出所有商品
        for num,goods in enumerate(goods_list,1):
            print(num,goods)
        print('----输入q退出购买')

        choice = input('请输入商品编号(结账输入q):').strip()


        #判断输入的是符合的数字,只是选购功能，都放在购物车里面，没有结算
        if choice.isdigit() and 4>=int(choice)>=1:
            num = input('请输入你需要购买的数量:')
            # 获取商品名称和单价
            goods, price = goods_list[int(choice) - 1]
            #判断用户余额是否大于商品单价
            if user_balance >= price:
                #花费
                money = price * int(num)
                #判断用户余额是否大于总花费
                if user_balance >= money:
                    #用户消费
                    if goods not in shop_car:
                        shop_car[goods] = num
                    else:
                        shop_car[goods] += num
                    count+=money

                else:
                    print('余额买不了这么多东西')
            else:
                print('余额不足单价')

        #判断是否需要结账
        elif choice == 'q':
            commint = input('是否确认结账，请输入y/n:')
            if commint == 'y':
                #调用商城购物车支付功能，并调用银行支付接口
                flag,msg = shop_interface.buy_shop_interface(user_info['user'],count)
                if flag:
                    print(msg)
                    break
                else:
                    print(msg)
            #如果不支付就把商品全部加到用户的购物车信息里面
            elif commint == 'n':
                flag,msg = shop_interface.add_shop_car_interface(user_info['user'],shop_car)
                if flag:
                    print(msg)
                    break
        else:
            print('请输入正确的数字')


#查看购物车
@common.login_auth
def check_shop_cart():
    flag = shop_interface.check_shop_car_interface(user_info['user'])
    if not flag:
        print('购物车是空的，请去选择商品')
    else:
        print(flag)
#注销
@common.login_auth
def logout():
    flag = user_interface.logout_interface()
    print(flag)

#冻结用户
def lock_user():
    while True:
        lock_user = input('请输入需要冻结的用户:')
        #查询需要冻结的用户是否存在
        flag = user_interface.register_interface_select(lock_user)
        if not flag:
            print('冻结的用户不存在')
            continue
        else:
            flag,msg = user_interface.lock_user_interface(lock_user)
            if flag:
                print(msg)
                break

#解冻用户
def unlock_user():
    while True:
        unlock_user = input('请输入需要解冻的用户:')
        #查询需要解冻的用户是否存在
        flag = user_interface.register_interface_select(unlock_user)
        if not flag:
            print('解冻的用户不存在')
            continue
        else:
            flag,msg = user_interface.unlock_user_interface(unlock_user)
            if flag:
                print(msg)
                break


#修改额度
def change_limit():
    while True:
        change_user = input('请输入需要修改额度的用户:')
        #查询需要解冻的用户是否存在
        flag = user_interface.register_interface_select(change_user)
        if not flag:
            print('该用户不存在')
            continue
        change_limit_money = input('请输入修改的金额:')
        flag,msg = user_interface.change_limit_interface(user_info['user'],change_limit_money)
        if flag:
            print(msg)


admin_func_dic = {
    '1': lock_user,
    '2': unlock_user,
    '3': change_limit,
}

#管理员功能
@common.login_auth
def admin_sys():
    while True:
        print('''
        1.冻结用户
        2.解冻用户
        3.用户额度
        ''')

        choice = input('请选择管理员功能: ').strip()

        if choice not in admin_func_dic:
            print('请重新输入')
            continue

        admin_func_dic[choice]()


func_dic = {
    '1': register,
    '2': login,
    '3': check_bal,
    '4': withdraw,
    '5': repay,
    '6': transfer,
    '7': check_flow,
    '8': shopping,
    '9': check_shop_cart,
    '10': logout,
    '11': admin_sys,
}


def run():
    while True:
        print("""
        1  注册
        2  登陆
        3  查看余额
        4  提现
        5  还款
        6  转账
        7  查看流水
        8  购物车功能
        9  查看购物车
        10 注销
        11 管理员功能
        """)
        choice = input('请输入你的选择:').strip()
        if choice in func_dic:
            func_dic.get(choice)()
        elif choice == 'q':
            break
        else:
            print('请输入正确选项...')






