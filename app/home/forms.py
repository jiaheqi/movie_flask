#!/usr/bin/env python
# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, EqualTo, Email, Regexp, ValidationError
from app.model.user import User


class RegistForm(FlaskForm):
    """会员注册表单"""
    name = StringField(
        label=u"昵称",
        validators=[
            DataRequired(u"请输入昵称！")
        ],
        description=u"昵称",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入昵称！",
        }
    )
    email = StringField(
        label=u"邮箱",
        validators=[
            DataRequired(u"请输入邮箱！"),
            Email(u"邮箱格式不正确！")
        ],
        description=u"邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"邮箱！",
        }
    )
    phone = StringField(
        label=u"手机",
        validators=[
            DataRequired(u"请输入手机！"),
            Regexp("1[34578]\\d{9}", message=u"手机格式不正确！")
        ],
        description=u"手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"手机！",
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"请输入你的密码！")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入密码！",
        }
    )
    repwd = PasswordField(
        label=u"确认密码",
        validators=[
            DataRequired(u"请输入确认密码！"),
            EqualTo('pwd', message=u"两次密码不一致")
        ],
        description=u"确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入确认密码！",
        }
    )
    submit = SubmitField(
        u'注册',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )

    def validate_name(self, field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user == 1:
            raise ValidationError(u"昵称已存在！")

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(name=email).count()
        if user == 1:
            raise ValidationError(u"邮箱已存在！")

    def validate_phone(self, field):
        phone = field.data
        user = User.query.filter_by(name=phone).count()
        if user == 1:
            raise ValidationError(u"手机号已存在！")


class LoginForm(FlaskForm):
    """会员登录表单"""
    name = StringField(
        label=u"账号",
        validators=[
            DataRequired(u"请输入账号！")
        ],
        description=u"账号",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入账号！",
        }
    )
    pwd = PasswordField(
        label=u"密码",
        validators=[
            DataRequired(u"请输入你的密码！")
        ],
        description=u"密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": u"请输入密码！",
        }
    )
    submit = SubmitField(
        u'登录',
        render_kw={
            "class": "btn btn-lg btn-primary",
        }
    )


class UserdetailForm(FlaskForm):
    """会员修改表单"""
    name = StringField(
        label=u"昵称",
        validators=[
            DataRequired(u"请输入昵称！")
        ],
        description=u"昵称",
        render_kw={
            "class": "form-control",
            "placeholder": u"请输入昵称！",
        }
    )
    email = StringField(
        label=u"邮箱",
        validators=[
            DataRequired(u"请输入邮箱！"),
            Email(u"邮箱格式不正确！")
        ],
        description=u"邮箱",
        render_kw={
            "class": "form-control",
            "placeholder": u"邮箱！",
        }
    )
    phone = StringField(
        label=u"手机",
        validators=[
            DataRequired(u"请输入手机！"),
            Regexp("1[34578]\\d{9}", message=u"手机格式不正确！")
        ],
        description=u"手机",
        render_kw={
            "class": "form-control",
            "placeholder": u"手机！",
        }
    )
    face = FileField(
        label=u"头像",
        validators=[
            DataRequired(u"请上传头像")
        ],
    )
    info = TextAreaField(
        label=u"简介",
        validators=[
            DataRequired(u"请输入简介！")
        ],
        description=u"简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    submit = SubmitField(
        u'保存修改',
        render_kw={
            "class": "btn btn-success",
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
        u'修改密码',
        render_kw={
            "class": "btn btn-success",
        }
    )


class CommentForm(FlaskForm):
    content = TextAreaField(
        label=u'内容',
        validators=[
            DataRequired(u"请输入内容！")
        ],
        description=u'内容',
        render_kw={
            "id": "input_content",
        }
    )
    submit = SubmitField(
        u'提交评论',
        render_kw={
            "class": "btn btn-success",
            "id": "btn-sub",
        }
    )

