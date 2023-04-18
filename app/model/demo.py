# demo
from datetime import datetime

from app import db


class Demo(db.Model):
    __tablename__ = 'demo'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    bussType = db.Column(db.Integer,  unique=True)  # 交易类型
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    remark = db.Column(db.String(100), unique=True)
    htmlfile = db.Column(db.String(100), unique=True)

    def __repr__(self):
        return "<Demo %r>" % self.name