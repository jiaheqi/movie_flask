# 权限
from datetime import datetime

from app.model.base import db



class Auth(db.Model):
    __tablename__ = 'auth'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 名字
    url = db.Column(db.String(255), unique=True)  # 地址
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name