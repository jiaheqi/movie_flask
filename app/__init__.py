# !/usr/bin/env python
# #coding:utf-8
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
# import SQLAlchemy
import os
#
#
app = Flask(__name__)
# paytest的db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pay123123@192.168.185.36:3306/paytest'
# app.config['SQLALCHEMY_BINDS'] = 'mysql+pymysql://pay_account_test:303b7fa84f92d28c@test-teg-pay.db.58dns.org:53494' \
#                                  '/dbwww58com_pay '
app.config['SQLALCHEMY_BINDS'] = {
    'pmc_merinfo': 'mysql+pymysql://pay_account_test:303b7fa84f92d28c@test-teg-pay.db.58dns.org:53494/dbwww58com_pay'}
app.config['SECRET_KEY'] = "af2fad8cfe1f4c5fac4aa5edf6fcc8f3"
app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")  # 定义一个上传路径
app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")  # 定义一个上传路径
app.config['DEMO_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates/admin/")  # 定义一个demo上传路径
app.debug = True
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("home/404.html"), 404
#
#
# def create_app():
#     app = Flask(__name__)
#     # paytest的db
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pay123123@192.168.185.36:3306/paytest'
#     # app.config['SQLALCHEMY_BINDS'] = 'mysql+pymysql://pay_account_test:303b7fa84f92d28c@test-teg-pay.db.58dns.org:53494' \
#     #                                  '/dbwww58com_pay '
#     app.config['SQLALCHEMY_BINDS'] = {
#         'pmc_merinfo': 'mysql+pymysql://pay_account_test:303b7fa84f92d28c@test-teg-pay.db.58dns.org:53494/dbwww58com_pay'}
#     app.config['SECRET_KEY'] = "af2fad8cfe1f4c5fac4aa5edf6fcc8f3"
#     app.config['UP_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")  # 定义一个上传路径
#     app.config['FC_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/users/")  # 定义一个上传路径
#     app.config['DEMO_DIR'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),
#                                           "static/uploads/demos/")  # 定义一个demo上传路径
#     app.debug = True
#     register_blueprint(app)
#     db = SQLAlchemy(app)
#     # from app.home import home as home_blueprint
#     # from app.admin import admin as admin_blueprint
#     # app.register_blueprint(home_blueprint)
#     # app.register_blueprint(admin_blueprint, url_prefix='/admin')
#     return app,db
#
#
# # def register_blueprint(app):
# #     from app.home import home as home_blueprint
# #     from app.admin import admin as admin_blueprint
# #     app.register_blueprint(home_blueprint)
# #     app.register_blueprint(admin_blueprint, url_prefix='/admin')
# #     return home_blueprint,admin_blueprint
