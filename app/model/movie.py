# 电影
from datetime import datetime

from app.model.base import db



class Movie(db.Model):
    __tablename__ = 'movie'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # 编号
    title = db.Column(db.String(255), unique=True)  # 标题
    url = db.Column(db.String(255), unique=True)  # 地址
    info = db.Column(db.Text)  # 简介
    logo = db.Column(db.String(255), unique=True)  # 封面
    star = db.Column(db.SmallInteger)  # 星级
    playnum = db.Column(db.BigInteger)  # 播放量
    commentnum = db.Column(db.BigInteger)  # 评论量
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  # 所属标签
    area = db.Column(db.String(255))  # 上映地区
    release_time = db.Column(db.Date)  # 上映时间
    length = db.Column(db.String(100))  # 播放时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 添加时间
    comments = db.relationship('Comment', backref='movie')  # 会员日志外键关系关联
    moviecols = db.relationship('Moviecol', backref='movie')  # 收藏外键关系关联

    def __repr__(self):
        return "<Movie %r>" % self.title