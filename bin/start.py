# -*- conding:utf-8 -*-
#启动文件代码
import os
import sys
# 获取项目文件的根目录
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#把根目录加入到环境变量中
sys.path.append(BASE_DIR)
from core import src

if __name__ == '__main__':
    src.run()







