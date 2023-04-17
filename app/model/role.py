# 角色
from datetime import datetime

from app.model.base import db



class Role(db.Model):
    __tablename__ = 'role'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名字
    auths = db.Column(db.String(600))  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    admins = db.relationship('Admin', backref='role')  # 收藏外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name