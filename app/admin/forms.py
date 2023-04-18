#!/usr/bin/env python
# coding:utf-8
from enum import Enum

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, ValidationError, EqualTo


# tags = Tag.query.all()
# auth_list = Auth.query.all()
# role_list = Role.query.all()
# from app.model.bussType import BussType


# class Enum(FlaskForm):
#     busstype_list = BussType.query.order_by(BussType.id.desc())
# #     # busstype_list =


class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField(
        label=u"账号",
        validators=[
            DataRequired(u"请输入你的账号！")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入账号！",
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"请输入你的密码！")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入密码！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        u'登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    def validate_account(self, field):
        account = field.data
        # admin = Admin.query.filter_by(name=account).count()
        # if admin == 0:
        #     raise ValidationError(u"账号不存在！")


class TagForm(FlaskForm):
    """标签"""
    name = StringField(
        label=u"标签",
        validators=[
            DataRequired(u"请输入标签！")
        ],
        description=u"标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": u"请输入标签名称！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        u'添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class MovieForm(FlaskForm):
    """片名"""
    title = StringField(
        label=u"片名",
        validators=[
            DataRequired(u"请输入片名！")
        ],
        description=u"片名",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入片名！",
        }
    )
    url = FileField(
        label=u"文件",
        validators=[
            DataRequired(u"请上传文件！")
        ],
        description=u"文件",

    )
    info = TextAreaField(
        label=u"简介",
        validators=[
            DataRequired(u"请输入简介！")
        ],
        description=u"简介",
        render_kw={
            "class": "form-control",
            "rows": 10,
        }
    )
    logo = FileField(
        label=u"封面",
        validators=[
            DataRequired(u"请上传封面！")
        ],
        description=u"封面",
    )
    star = SelectField(
        label=u"星级",
        validators=[
            DataRequired(u"请选择星级！")
        ],
        coerce=int,
        choices=[(1, u"1星"), (2, u"2星"), (3, u"3星"), (4, u"4星"), (5, u"5星")],
        description=u"星级",
        render_kw={
            "class": "form-control",
        }
    )
    tag_id = SelectField(
        label=u"标签",
        validators=[
            DataRequired(u"请选择标签！")
        ],
        coerce=int,
        # choices=[(v.id, v.name) for v in tags],
        choices=[],
        description=u"标签",
        render_kw={
            "class": "form-control",
        }
    )
    area = StringField(
        label=u"地区",
        validators=[
            DataRequired(u"请输入地区！")
        ],
        description=u"地区",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入地区！",
        }
    )
    length = StringField(
        label=u"片长",
        validators=[
            DataRequired(u"请输入片长！")
        ],
        description=u"片长",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入片长！",
        }
    )
    release_time = StringField(
        label=u"上映时间",
        validators=[
            DataRequired(u"请选择上映时间！")
        ],
        description=u"上映时间",
        render_kw={
            "class": "form-control",
            "placeholder": u"请选择上映时间！",
            "id": "input_release_time"
        }
    )
    submit = SubmitField(
        u'添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class PreviesForm(FlaskForm):
    title = StringField(
        label=u"预告标题",
        validators=[
            DataRequired(u"请输入预告标题！")
        ],
        description=u"预告标题",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入预告标题！",
        }
    )
    logo = FileField(
        label=u"预告封面",
        validators=[
            DataRequired(u"请上传预告封面！")
        ],
        description=u"预告封面",

    )
    submit = SubmitField(
        u'添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label=u"旧密码",
        validators=[
            DataRequired(u"请输入旧密码！")
        ],
        description=u"旧密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入旧密码！",
        }
    )
    new_pwd = PasswordField(
        label=u"新密码",
        validators=[
            DataRequired(u"请输入新密码！")
        ],
        description=u"新密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入新密码！",
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )

    # def validate_old_pwd(self, field):
    #     from flask import session
    #     pwd = field.data
    #     print pwd
    #     print session
    #     name = session["admin"]
    #     admin = Admin.query.filter_by(
    #         name=name
    #     ).first()
    #     if not admin.check_pwd(pwd):
    #         raise ValidationError(u"旧密码错误")


class AuthForm(FlaskForm):
    name = StringField(
        label=u"权限名称",
        validators=[
            DataRequired(u"请输入权限名称！")
        ],
        description=u"权限名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入权限名称！",
            # "required": "required"
        }
    )
    url = StringField(
        label=u"权限地址",
        validators=[
            DataRequired(u"请输入权限地址！")
        ],
        description=u"权限地址",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入权限地址！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class RoleForm(FlaskForm):
    name = StringField(
        label=u"角色名称",
        validators=[
            DataRequired(u"请输入角色名称！")
        ],
        description=u"角色名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入角色名称！",

            # "required": "required"
        }
    )
    auths = SelectMultipleField(
        label=u"权限列表",
        validators=[
            DataRequired(u"请选择权限列表")
        ],
        coerce=int,
        # choices=[(v.id, v.name) for v in auth_list],
        choices=[],
        description=u"权限名称",
        render_kw={
            "class": "form-control",
            "type": "checkbox",
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class AdminForm(FlaskForm):
    """管理员登录表单"""
    name = StringField(
        label=u"管理员名称",
        validators=[
            DataRequired(u"请输入管理员名称！")
        ],
        description=u"管理员名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入管理员名称！",
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label=u"管理员密码",
        validators=[
            DataRequired(u"请输入管理员密码！")
        ],
        description=u"管理员密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入管理员密码！",
            # "required": "required"
        }
    )
    repwd = PasswordField(
        label=u"管理员重复密码",
        validators=[
            DataRequired(u"请输入管理员重复密码！"),
            EqualTo('pwd', message=u"两次密码不一致")
        ],
        description=u"管理员重复密码",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入管理员重复密码！",
            # "required": "required"
        }
    )
    role_id = SelectField(
        label=u"所属角色",
        coerce=int,
        # choices=[(v.id, v.name) for v in role_list],
        choices=[],
        render_kw={
            "class": "form-control",
        }
    )
    submit = SubmitField(
        u'编辑',
        render_kw={
            "class": "btn btn-primary",
        }
    )


class DemoForm(FlaskForm):
    name = StringField(
        label=u"demo名称",
        validators=[
            DataRequired(u"请输入demo名称！")
        ],
        description=u"demo名称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入demo名称！",
        }
    )
    remark = StringField(
        label=u"备注和描述",
        validators=[
            DataRequired(u"请输入备注和描述！")
        ],
        description=u"备注和描述",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入备注和描述！",
            "rows": 10,
        }
    )
    busstype = SelectField(
        label=u"交易类型",
        coerce=int,
        # choices=[(v.id, v.name) for v in Enum.busstype_list],
        choices=[(1, u"支付"), (2, u"充值"), (3, u"转账"), (4, u"打款"), (5, u"冻结")],
        render_kw={
            "class": "form-control",
        }
    )
    logo = FileField(
        label=u"demo文件",
        validators=[
            DataRequired(u"请上传demo文件！")
        ],
        description=u"demo文件",

    )
    submit = SubmitField(
        u'添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )
