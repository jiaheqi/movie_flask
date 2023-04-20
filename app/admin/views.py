#!/usr/bin/env python
# #coding:utf-8
# from app import admin
import datetime
import json
import os
import uuid
from functools import wraps

import requests
from flask import render_template, url_for, redirect, flash, session, jsonify
from flask import request
from werkzeug.utils import secure_filename

from manage import app

from app.admin.forms import LoginForm, TagForm, MovieForm, PreviesForm, PwdForm, AuthForm, RoleForm, AdminForm, DemoForm
from app.model.admin import Admin
from app.model.demo import Demo
from app.model.tag import Tag

from . import admin

# 上下文应用处理器
# from .mysqldb import Mysqlcon
from .. import db
from ..model.adminlog import Adminlog
from ..model.auth import Auth
from ..model.comment import Comment
from ..model.merinfo import MerInfo
from ..model.movie import Movie
from ..model.moviecol import Moviecol
from ..model.oplog import Oplog
from ..model.preview import Preview
from ..model.role import Role
from ..model.user import User
from ..model.userlog import Userlog


@admin.context_processor
def tpl_extra():
    data = dict(
        online_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )
    return data


# 登录装饰器
def admin_login_req(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)

    return decorated_function


# # 权限控制装饰器
# def admin_auth(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         admin = Admin.query.join(
#             Role
#         ).filter(
#             Role.id == Admin.role_id,
#             Admin.id == session['admin_id']
#         ).first()
#         auths = admin.role.auths
#         auths = list(map(lambda v: int(v), auths.split(',')))
#         auth_list = Auth.query.all()
#         urls = [v.url for v in auth_list for val in auths if val == v.id]
#         rule = request.url_rule
#         if str(rule) not in urls:
#             abort(404)
#         return f(*args, **kwargs)
#
#     return decorated_function


# 修改文件名称
def change_filename(filename):
    fileinfo = os.path.splitext(filename)
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


# 获取文件路径
def set_htmlfilepath(busstype, filename):
    if busstype == 1:
        filename = "pay/" + filename
    elif busstype == 2:
        filename = "recharge/" + filename
    return filename


@admin.route('/')
@admin_login_req
def index():
    return render_template("admin/index.html")


# 登录
@admin.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        print(data)
        # admin = Admin.query.filter_by(name=data["account"]).first()
        # if not admin.check_pwd(data["pwd"]):
        #     flash(u"密码错误", "err")
        #     return redirect(url_for("admin.login"))
        # session["admin"] = data["account"]
        # session["admin_id"] = admin.id
        # adminlog = Adminlog(
        #     admin_id=admin.id,
        #     ip=request.remote_addr
        # )
        # db.session.add(adminlog)
        # db.session.commit()
        return render_template("admin/index.html")
    return render_template("admin/login.html", form=form)


# 退出登录
@admin.route('/logout/')
@admin_login_req
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))


# 修改密码
@admin.route('/pwd/', methods=['GET', 'POST'])
@admin_login_req
def pwd():
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=session["admin"]).first()
        if not admin.check_pwd(data['old_pwd']):
            flash(u"旧密码错误", "err")
            return redirect(url_for("admin.pwd"))
        from werkzeug.security import generate_password_hash
        admin.pwd = generate_password_hash(data['new_pwd'])
        db.session.add(admin)
        db.session.commit()
        flash(u"修改密码成功，请重新登录", "ok")
        return redirect(url_for("admin.logout"))
    return render_template("admin/pwd.html", form=form)


# 添加标签
@admin.route('/tag/add/', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag = Tag.query.filter_by(name=data["name"]).count()
        if tag == 1:
            flash(u"名称已经存在", "err")
            return redirect(url_for("admin.tag_add"))
        tag = Tag(
            name=data["name"]
        )
        db.session.add(tag)
        db.session.commit()
        flash(u"添加标签成功", "ok")
        oplog = Oplog(
            admin_id=session["admin_id"],
            ip=request.remote_addr,
            reason=u"添加标签%s" % data["name"]
        )
        db.session.add(oplog)
        db.session.commit()
        redirect(url_for("admin.tag_add"))
    return render_template("admin/tag_add.html", form=form)


# 编辑标签
@admin.route('/tag/edit/<int:id>', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def tag_edit(id=None):
    form = TagForm()
    tag = Tag.query.get_or_404(id)  # id=1 科幻所在的对象
    if form.validate_on_submit():
        data = form.data  # 这个date是我看你想修改成啥
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag.name != data["name"] and tag_count == 1:
            flash(u"名称已经存在", "err")
            return redirect(url_for("admin.tag_edit", id=id))
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash(u"修改标签成功", "ok")
        redirect(url_for("admin.tag_edit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


# 标签列表
@admin.route('/tag/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def tag_list(page=None):
    if page is None:
        page = 1
    # page_data = Tag.query.order_by(
    #     Tag.addtime.desc()
    # ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    page_data = Tag.query.order_by(Tag.addtime.desc()).paginate(page=page)
    return render_template("admin/tag_list.html", page_data=page_data)


# 充值demo列表
@admin.route('/tag/demoRecharge/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def demo_recharge(page=None):
    if page is None:
        page = 1
    # page_data = Tag.query.order_by(
    #     Tag.addtime.desc()
    # ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    page_data = Demo.query.filter_by(bussType=2).order_by(Demo.addtime.desc()).paginate(page=page)
    print(page_data)
    print(type(page_data))
    return render_template("admin/demo_recharge.html", page_data=page_data)


# 支付demo
@admin.route('/tag/demoPay/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def demo_pay(page=None):
    if page is None:
        page = 1
    # page_data = Tag.query.order_by(
    #     Tag.addtime.desc()
    # ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    print(1)
    page_data = Demo.query.filter_by(bussType=1).order_by(Demo.addtime.desc()).paginate(page=page)
    print(page_data)
    return render_template("admin/demo_pay.html", page_data=page_data)


# 发起请求
@admin.route('/wb_demorequest/<int:id>', methods=['GET'])
def demo_request(id=None):
    page_data = Demo.query.filter_by(id=id).first_or_404()
    req_path = page_data.htmlfile
    return render_template(req_path)


# 添加demo
@admin.route('/tag/demoRecharge/add/', methods=['GET', 'POST'])
def demo_add():
    form = DemoForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        # print form.logo.data.filename
        # print file_logo
        if not os.path.exists(app.config["DEMO_DIR"]):
            os.makedirs(app.config["DEMO_DIR"])
            os.chmod(app.config["DEMO_DIR"], "rw")
        busstype = data["busstype"]
        logo = set_htmlfilepath(busstype, file_logo)
        form.logo.data.save(app.config["DEMO_DIR"] + logo)
        logo = "admin/" + logo
        print(data)
        demo = Demo(
            name=data["name"],
            remark=data["remark"],
            htmlfile=logo,
            bussType=busstype
        )
        db.session.add(demo)
        db.session.commit()
        flash(u"添加demo成功！", "ok")
        return redirect(url_for("admin.demo_add", demo=demo))
    return render_template("admin/demo_add.html", form=form)


# 修改demo
@admin.route('/demo/edit/<int:id>/', methods=['GET', 'POST'])
def demo_edit(id):
    form = DemoForm()
    form.logo.validators = []
    demo = Demo.query.get_or_404(int(id))
    # 回显当前记录的数据
    if request.method == 'GET':
        form.name.data = demo.name
        form.remark.data = demo.remark
        form.busstype.data = demo.bussType
    if form.validate_on_submit():
        data = form.data
        demo.name = data["name"]
        demo.remark = data["remark"]
        demo.bussType = data["bussType"]
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            demo.htmlfile = set_htmlfilepath(file_logo)
            form.logo.data.save(app.config["DEMO_DIR"] + demo.logo)
        db.session.add(demo)
        db.session.commit()
        flash(u"修改demo成功！", "ok")
        return redirect(url_for("admin.demo_edit", id=id))
    return render_template("admin/demo_edit.html", form=form, demo=demo)


@admin.route('/merinfo_list/<int:page>', methods=['GET'])
def merinfo_list(page=None):
    if page is None:
        page = 1
    # dbpmc,cursor = Mysqlcon.conn(Mysqlcon)
    # sql = "SELECT id,mer_key FROM dbwww58com_pay.mer_info WHERE id = 1000"
    # res = cursor.execute(sql)
    # page_data = cursor.fetchall()
    # print(page_data)
    page_data = MerInfo.query.filter_by(id=1000).order_by(MerInfo.id.desc()).paginate(page=page)
    return render_template("admin/merinfo_list.html", page_data=page_data)


# # 充值demo添加
# def demo_add():
#     form = DemoForm()
#     if form.validate_on_submit():
#         data = form.data
#         demo = Demo.query.filter_by(name=data["name"]).count()
#         if demo == 1:
#             flash(u"名称已经存在", "err")
#             return redirect(url_for("admin.tag_add"))
#         demo = Demo(
#             name=data["name"]
#         )
#         db.session.add(demo)
#         db.session.commit()
#         flash(u"添加标签成功", "ok")
#         oplog = Oplog(
#             admin_id=session["admin_id"],
#             ip=request.remote_addr,
#             reason=u"添加标签%s" % data["name"]
#         )
#         db.session.add(oplog)
#         db.session.commit()
#         redirect(url_for("admin.demo_add"))
#     return render_template("admin/demo_add.html", form=form)


# 标签删除
@admin.route('/tag/del/<int:id>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def tag_del(id=None):
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)
    db.session.commit()
    flash(u"删除标签成功", "ok")
    return redirect(url_for("admin.tag_list", page=1))


# 增加电影
@admin.route('/movie/add/', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def movie_add():
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data["title"],
            url=url,
            info=data["info"],
            logo=logo,
            star=int(data["star"]),
            playnum=0,
            commentnum=0,
            tag_id=int(data["tag_id"]),
            area=data["area"],
            release_time=data["release_time"],
            length=data["length"]
        )
        db.session.add(movie)
        db.session.commit()
        flash(u"添加电影成功！", "ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add.html", form=form)


# 电影列表
@admin.route('/movie/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def movie_list(page=None):
    if page is None:
        page = 1
    page_data = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id
    ).order_by(
        Movie.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/movie_list.html", page_data=page_data)


# 删除电影
@admin.route('/movie/del/<int:id>/', methods=['GET'])
@admin_login_req
# @admin_auth
def movie_del(id=None):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash(u"删除电影成功", "ok")
    return redirect(url_for("admin.movie_list", page=1))


# 编辑电影
@admin.route('/movie/edit/<int:id>', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def movie_edit(id=None):
    form = MovieForm()
    form.url.validators = []
    form.logo.validators = []
    movie = Movie.query.get_or_404(int(id))  # id=1 空战1所在的对象
    if request.method == "GET":
        form.info.data = movie.info
        form.tag_id.data = movie.tag_id
        form.star.data = movie.star
    if form.validate_on_submit():
        data = form.data  # 这个date是我看你想修改成啥
        movie_count = Movie.query.filter_by(title=data["title"]).count()  # 我去库里查下你要改的这个东西有没有
        if movie.title != data["title"] and movie_count == 1:
            flash(u"片名已经存在", "err")
            return redirect(url_for("admin.movie_edit", id=id))

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        if form.url.data.filename != "":
            file_url = secure_filename(form.url.data.filename)
            movie.url = change_filename(file_url)
            form.url.data.save(app.config["UP_DIR"] + movie.url)
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            movie.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + movie.logo)
        movie.star = data["star"]
        movie.tag_id = data["tag_id"]
        movie.info = data["info"]
        movie.title = data["title"]
        movie.area = data["area"]
        movie.length = data["length"]
        movie.release_time = data["release_time"]
        db.session.add(movie)
        db.session.commit()
        flash(u"修改电影成功", "ok")
        redirect(url_for("admin.movie_edit", id=movie.id))
    return render_template("admin/movie_edit.html", form=form, movie=movie)


# 预告管理
@admin.route('/preview/add/', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def preview_add():
    form = PreviesForm()
    if form.validate_on_submit():
        data = form.data
        file_logo = secure_filename(form.logo.data.filename)
        # print form.logo.data.filename
        # print file_logo
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        logo = change_filename(file_logo)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        preview = Preview(
            title=data["title"],
            logo=logo
        )
        db.session.add(preview)
        db.session.commit()
        flash(u"添加預告成功！", "ok")
        return redirect(url_for("admin.preview_add", preview=preview))
    return render_template("admin/preview_add.html", form=form)


# 预告列表
@admin.route('/preview/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def preview_list(page=None):
    if page is None:
        page = 1
    page_data = Preview.query.filter_by().order_by(
        Preview.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/preview_list.html", page_data=page_data)


# 预告删除
@admin.route('/preview/del/<int:id>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def preview_del(id=None):
    preview = Preview.query.get_or_404(int(id))
    db.session.delete(preview)
    db.session.commit()
    flash(u"删除预告成功", 'ok')
    return redirect(url_for('admin.preview_list', page=1))


# 预告管理
@admin.route('/preview/edit/<int:id>/', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def preview_edit(id):
    form = PreviesForm()
    form.logo.validators = []
    preview = Preview.query.get_or_404(int(id))
    if request.method == 'GET':
        form.title.data = preview.title
    if form.validate_on_submit():
        data = form.data
        preview.title = data["title"]
        if form.logo.data.filename != "":
            file_logo = secure_filename(form.logo.data.filename)
            preview.logo = change_filename(file_logo)
            form.logo.data.save(app.config["UP_DIR"] + preview.logo)
        db.session.add(preview)
        db.session.commit()
        flash(u"修改預告成功！", "ok")
        return redirect(url_for("admin.preview_edit", id=id))
    return render_template("admin/preview_edit.html", form=form, preview=preview)


# 用户列表
@admin.route('/user/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def user_list(page=None):
    if page is None:
        page = 1
    page_data = User.query.filter_by().order_by(
        User.id.asc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/user_list.html", page_data=page_data)


# 用户查看
@admin.route('/user/view/<int:id>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def user_view(id=None):
    user = User.query.get_or_404(int(id))
    return render_template("admin/user_view.html", user=user)


# 用户删除
@admin.route('/user/del/<int:id>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def user_del(id=None):
    user = User.query.get_or_404(int(id))
    db.session.delete(user)
    db.session.commit()
    flash(u"删除会员成功", 'ok')
    return redirect(url_for('admin.user_list', page=1))


# 评论列表
@admin.route('/comment/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def comment_list(page=None):
    if page is None:
        page = 1
    page_data = Comment.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Comment.movie_id,
        User.id == Comment.user_id
    ).order_by(
        Comment.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/comment_list.html", page_data=page_data)


# 评论删除
@admin.route('/comment/del/<int:id>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def comment_del(id=None):
    comment = Comment.query.get_or_404(int(id))
    db.session.delete(comment)
    db.session.commit()
    flash(u"删除评论成功", 'ok')
    return redirect(url_for('admin.comment_list', page=1))


# 收藏列表
@admin.route('/moviecol/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def moviecol_list(page=None):
    if page is None:
        page = 1
    page_data = Moviecol.query.join(
        Movie
    ).join(
        User
    ).filter(
        Movie.id == Moviecol.movie_id,
        User.id == Moviecol.user_id
    ).order_by(
        Moviecol.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/moviecol_list.html", page_data=page_data)


# 收藏删除
@admin.route('/moviecol/del/<int:id>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def moviecol_del(id=None):
    moviecol = Moviecol.query.get_or_404(int(id))
    db.session.delete(moviecol)
    db.session.commit()
    flash(u"删除收藏成功", 'ok')
    return redirect(url_for('admin.moviecol_list', page=1))


# 操作日志
@admin.route('/oplog/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def oplog_list(page=None):
    if page is None:
        page = 1
    page_data = Oplog.query.join(
        Admin
    ).filter(
        Admin.id == Oplog.admin_id,
    ).order_by(
        Oplog.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/oplog_list.html", page_data=page_data)


# 管理员日志
@admin.route('/adminloginlog/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def adminloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Adminlog.query.join(
        Admin
    ).filter(
        Admin.id == Adminlog.admin_id,
    ).order_by(
        Adminlog.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/adminloginlog_list.html", page_data=page_data)


# 用户日志
@admin.route('/userloginlog/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def userloginlog_list(page=None):
    if page is None:
        page = 1
    page_data = Userlog.query.join(
        User
    ).filter(
        User.id == Userlog.user_id,
    ).order_by(
        Userlog.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/userloginlog_list.html", page_data=page_data)


# 添加角色
@admin.route('/role/add/', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def role_add():
    form = RoleForm()
    if form.validate_on_submit():
        data = form.data
        role = Role(
            name=data['name'],
            auths=','.join(map(lambda v: str(v), data['auths']))
        )
        db.session.add(role)
        db.session.commit()
        flash(u"添加角色成功", 'ok')
    return render_template("admin/role_add.html", form=form)


# 编辑角色
@admin.route('/role/edit/<int:id>', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def role_edit(id=None):
    form = RoleForm()
    role = Role.query.get_or_404(id)  # id=1 科幻所在的对象
    if request.method == 'GET':
        form.auths.data = list(map(lambda v: int(v), role.auths.split(',')))
    if form.validate_on_submit():
        data = form.data  # 这个date是我看你想修改成啥
        role.name = data['name']
        role.auths = ','.join(map(lambda v: str(v), data['auths']))
        db.session.add(role)
        db.session.commit()
        flash(u"修改标签成功", "ok")
        redirect(url_for("admin.role_edit", id=id))
    return render_template("admin/role_edit.html", form=form, role=role)


# 角色列表
@admin.route('/role/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def role_list(page=None):
    if page is None:
        page = 1
    page_data = Role.query.order_by(
        Role.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/role_list.html", page_data=page_data)


# 删除角色
@admin.route('/role/del/<int:id>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def role_del(id=None):
    role = Role.query.filter_by(id=id).first_or_404()
    db.session.delete(role)
    db.session.commit()
    flash(u"删除角色成功", 'ok')
    return redirect(url_for('admin.role_list', page=1))


# 权限添加
@admin.route('/auth/add/', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def auth_add():
    form = AuthForm()
    if form.validate_on_submit():
        data = form.data
        auth = Auth(
            name=data['name'],
            url=data['url']
        )
        db.session.add(auth)
        db.session.commit()
        flash(u"添加权限成功", 'ok')
    return render_template("admin/auth_add.html", form=form)


# 权限列表
@admin.route('/auth/list/<int:page>/', methods=['GET'])
@admin_login_req
# @admin_auth
def auth_list(page=None):
    if page is None:
        page = 1
    page_data = Auth.query.order_by(
        Auth.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/auth_list.html", page_data=page_data)


# 删除权限
@admin.route('/auth/del/<int:id>/', methods=['GET'])
@admin_login_req
# @admin_auth
def auth_del(id=None):
    auth = Auth.query.filter_by(id=id).first_or_404()  # auth = Auth.query.get_or_404(int(id))
    db.session.delete(auth)
    db.session.commit()
    flash(u"删除权限成功", 'ok')
    return redirect(url_for('admin.auth_list', page=1))


# 编辑权限
@admin.route('/auth/edit/<int:id>', methods=['GET', 'POST'])
@admin_login_req
# @admin_auth
def auth_edit(id=None):
    form = AuthForm()
    auth = Auth.query.get_or_404(id)  # id=1 科幻所在的对象
    if form.validate_on_submit():
        data = form.data  # 这个date是我看你想修改成啥
        auth.url = data['url']
        auth.name = data['name']
        db.session.add(auth)
        db.session.commit()
        flash(u"修改标签成功", "ok")
        redirect(url_for("admin.auth_edit", id=id))
    return render_template("admin/auth_edit.html", form=form, auth=auth)


# 添加管理员
@admin.route('/admin/add/', methods=['GET', 'POST'])
# @admin_login_req
# @admin_auth
def admin_add():
    form = AdminForm()
    from werkzeug.security import generate_password_hash
    if form.validate_on_submit():
        data = form.data
        admin = Admin(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
            role_id=data['role_id'],
            is_super=1
        )
        db.session.add(admin)
        db.session.commit()
        flash(u"添加管理员成功", "ok")
    return render_template("admin/admin_add.html", form=form)


# 管理员列表
@admin.route('/admin/list/<int:page>/', methods=['GET'])
# @admin_login_req
# @admin_auth
def admin_list(page=None):
    if page is None:
        page = 1
    page_data = Admin.query.join(
        Role
    ).filter(
        Role.id == Admin.role_id
    ).order_by(
        Admin.addtime.desc()
    ).paginate(page=page, per_page=10)  # 10代表每页显示多少
    return render_template("admin/admin_list.html", page_data=page_data)


@admin.route("/progress", methods=['GET'])
def get_progress():
    if request.method == "GET":

        memberid = request.args.get("memberid")
        env = request.args.get("env")

        if memberid == "":
            password = "Error! Please input memberid"

        else:
            password = env
        return jsonify({"password": password})


@admin.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
    return environ


def getMerkey(id=None):
    page_data = MerInfo.query.filter_by(id=id).first_or_404()
    merkey = page_data.mer_key
    return merkey


# 获取merkey方法
@admin.route('/getMerkeyAjax', methods=['POST'])
def getMerkeyAjax():
    # 获取前端json数据
    data = request.get_data()
    print(data)
    json_data = json.loads(data)
    print(json_data)
    userId = json_data.get("userId")
    merId = json_data.get("merId")

    # 给前端传输json数据
    info = dict()
    info['merkey'] = getMerkey(id=merId)
    print(info['merkey'])
    return jsonify(info)


import hashlib


def MD5encode(source):
    hexs = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a',
            'b', 'c', 'd', 'e', 'f']
    try:
        # 获得MD5摘要算法的 hashlib 对象
        digester = hashlib.md5()
        sbs = source.encode("UTF8")
        # 使用指定的字节更新摘要
        digester.update(sbs)
        rbs = digester.digest()
        # 把密文转换成十六进制的字符串形式
        j = len(rbs)
        result = []
        for i in range(j):
            b = rbs[i]
            result.append(hexs[b >> 4 & 0xf])
            result.append(hexs[b & 0xf])
        return ''.join(result)
    except Exception as e:
        return None


# 方法只能写在admin的views的文件中
@admin.route('/getMD5signAjax', methods=['POST'])
def getMD5signAjax():
    input_data = request.get_json()
    input_text = input_data['input']
    # 这里进行后台处理，比如将文本转为大写
    output_text = MD5encode(input_text)
    return jsonify({'MD5signResult': output_text})


@admin.route('/send_notification', methods=['POST'])
def send_notification():
    headers = {'Content-Type': 'application/json'}
    input_data = request.get_json()
    notification_url = input_data['notification_url']
    notification_params = input_data['notification_params']
    response = requests.post(notification_url, notification_params, headers)
    # 在这里模拟异步通知的发送，可以根据具体需求自定义
    # 例如使用requests库向通知URL发送POST请求，请求参数为notification_params
    print(response.status_code)
    print(response)
    status_code = response.status_code
    # if 200 == status_code:
    #     return '通知发送成功！'
    #
    # else:
    #     return '通知异常'
    return jsonify({'notifyResult': status_code})


@admin.route('/getBankTransferRecordResponse', methods=['GET'])
def reponsetest():
    orderid = datetime.now
    result = dict()
    result['code'] = '0'
    result['id'] = orderid
    return jsonify(result)
