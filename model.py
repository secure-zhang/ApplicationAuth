from __init__ import db
from _datetime import datetime

class Application(db.Model):
    __tablename__ = 'Application'
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),nullable=False,unique=True)
    userName = db.Column(db.String(64),nullable=False)
    phone = db.Column(db.String(11),nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    def __str__(self):
        return 'Application{userId=%s,userName=%s,phone=%s,}' % (self.userId, self.userName, self.phone)
class PhoneCode(db.Model):
    __tablename__ = 'PhoneCode'
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),db.ForeignKey('Application.userId'), nullable=True)
    code = db.Column(db.Integer(),nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __str__(self):
        return 'Application{user_Id=%s,code=%s,addTime=%s,}' % (self.user_Id, self.code, self.addTime)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except:
            return 0
    def __repr__(self):
        return '<User %r>' % (self.name)
if __name__ == '__main__':
    # db.create_all()
    # a = Application(userId='root',userName='张泽睿',phone='17635035787',addTime=datetime.now())
    # db.session.add(a)
    # a = Application.query.filter_by(userId='root').first()
    # p = PhoneCode(userId=a.userId,code=1234)
    # p.add()
    pass


