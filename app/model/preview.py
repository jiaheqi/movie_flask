# 上映预告
from datetime import datetime

from app.model.base import db



class Preview(db.Model):
    __tablename__ = 'preview'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    logo = db.Column(db.String(255), unique=True)  # 封面
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" % self.title