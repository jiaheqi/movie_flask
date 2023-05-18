#!/usr/bin/env python
# #coding:utf-8
import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask import render_template

from app import app

# 启动文件
if __name__ == '__main__':
    # 配置host=0.0.0.0是为了实现可以用过本机的IP来访问服务的地址
    app.run(host='0.0.0.0', port=20001, threaded=True)
    # app.run()

