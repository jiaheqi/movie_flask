# 电影收藏
from datetime import datetime
from app.model.base import db



class Moviecol(db.Model):
    __tablename__ = 'moviecol'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))  # 所属电影
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属用户
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" % self.id