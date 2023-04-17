# 会员登录日志
from datetime import datetime

from app.model.base import db



class Userlog(db.Model):
    __tablename__ = 'userlog'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员编号
    ip = db.Column(db.String(100))  # 登陆ip
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 会员登陆时间

    def __repr__(self):
        return "<Userlog %r>" % self.id