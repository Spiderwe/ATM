# -*- conding:utf-8 -*-
#数据处理层
from conf import settings
import json
import os

#保存注册信息
def save(user_dict):
    # 把注册信息写入文件
    with open(r'%s/%s.json' % (settings.DB_PATH, user_dict['user']), 'w', encoding='utf-8') as f:
        res = json.dumps(user_dict,ensure_ascii=False)
        f.write(res)
        f.flush()

#查询用户名是否已经被注册,通过判断用户名的文件是否存在
def select(username):
    user_path = '%s/%s.json' %(settings.DB_PATH,username)
    #判断文件是否存在，不存在返回None
    if not os.path.exists(user_path):
        return
    #存在就会返回信息
    with open(user_path,'r',encoding='utf-8') as f:
        res = f.read()
        user_dict = json.loads(res)   #转换成python的格式数据
        return user_dict






