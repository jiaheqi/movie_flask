from app.model.base import db



class MerInfo(db.Model):
    __bind_key__ = 'pmc_merinfo'
    __tablename__ = 'mer_info'  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)  # merid
    mer_key = db.Column(db.String(100), primary_key=True, autoincrement=True, unique=True)  # merkey

    def __repr__(self):
        return "<MerInfo %r>" % self.name