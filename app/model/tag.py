# 标签
from datetime import datetime

from app.model.base import db


class Tag(db.Model):
    __tablename__ = 'tag'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    name = db.Column(db.String(100), unique=True)  # 标题
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    movies = db.relationship('Movie', backref='tag')  # 会员日志外键关系关联

    def __repr__(self):
        return "<Tag %r>" % self.name