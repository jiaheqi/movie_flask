# from flask import render_template, url_for, redirect, flash, session, abort, current_app
# from app.admin.forms import LoginForm, TagForm, MovieForm, PreviesForm, PwdForm, AuthForm, RoleForm, AdminForm
# from app.models import Admin, Tag, Movie, Preview, User, Comment, Moviecol, Oplog, Adminlog, Userlog, Auth, Role
# from flask import request
# from functools import wraps
# from app import db, app
# from werkzeug.utils import secure_filename
# import os, uuid, datetime
#
#
# # 标签
# class Demo(db.Model):
#     __tablename__ = 'demo'  # 表名
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
#     name = db.Column(db.String(100), unique=True)  # 标题
#     addtime = db.Column(db.DateTime, index=True, default=datetime.time)  # 添加时间
#
#     def __repr__(self):
#         return "<Demo %r>" % self.name
#
#
# def demo_request(id = None):
#     demo = Demo.query.filter_by(id=id).first_or_404()
#     return demo
#
#
# if __name__ == '__main__':
#     print(demo_request(id =7))