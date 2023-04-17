# 操作日志
from datetime import datetime

from app.model.base import db



class Oplog(db.Model):
    __tablename__ = 'oplog'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 所属会员编号
    ip = db.Column(db.String(100))  # 登陆ip
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 会员登陆时间

    def __repr__(self):
        return "<Oplog %r>" % self.id