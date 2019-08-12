from __init__ import db
from _datetime import datetime
from flask_login._compat import unicode


class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),nullable=False,unique=True)
    userName = db.Column(db.String(64),nullable=False)
    phone = db.Column(db.String(11),nullable=False)
    isHandle = db.Column(db.Boolean(),nullable=False,default=False)
    handleName = db.Column(db.String(11),nullable=False,default='无')
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    def __str__(self):
        return 'Application{userId=%s,userName=%s,phone=%s,}' % (self.userId, self.userName, self.phone)
    def get_id(self):
        return unicode(self.id)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

class PhoneCode(db.Model):
    __tablename__ = 'PhoneCode'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),db.ForeignKey('User.userId'), nullable=False)
    code = db.Column(db.String(11),nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())

    def __str__(self):
        return 'Application{userId=%s,code=%s,addTime=%s,}' % (self.userId, self.code, self.addTime)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except:
            return 0

    def __repr__(self):
        return '<userId %r>' % (self.userId)

class UserData(db.Model):
    __tablename__ = 'UserData'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),db.ForeignKey('User.userId'), nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    zjs_1 = db.Column(db.Boolean(),nullable=False,default=False)
    nyzx_1 = db.Column(db.Boolean(),nullable=False,default=False)
    nyzx_2 = db.Column(db.Boolean(),nullable=False,default=False)
    sqs1 = db.Column(db.Boolean(),nullable=False,default=False)
    dss1 = db.Column(db.Boolean(),nullable=False,default=False)
    dss2 = db.Column(db.Boolean(),nullable=False,default=False)
    zss1 = db.Column(db.Boolean(),nullable=False,default=False)
    zss2 = db.Column(db.Boolean(),nullable=False,default=False)
    zjsbm = db.Column(db.Boolean(),nullable=False,default=False)
    nyzxbm = db.Column(db.Boolean(),nullable=False,default=False)
    jyqx = db.Column(db.Boolean(),nullable=False,default=False)
    jyjl = db.Column(db.Boolean(),nullable=False,default=False)
    qtjyqx = db.Column(db.Boolean(),nullable=False,default=False)
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except Exception as e:
            return 0
    def __repr__(self):
        return '<userId %r>' % (self.userId)

class UserImage(db.Model):
    __tablename__ = 'UserImage'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),db.ForeignKey('User.userId'), nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    fileName = db.Column(db.String(128))
    fileData = db.Column(db.LargeBinary(length=65536))
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except Exception as e:
            return 0
    def __repr__(self):
        return '<userId %r>' % (self.userId)
if __name__ == '__main__':
    # db.create_all()
    # a = User(userId='root2',userName='test',phone='17635035787',addTime=datetime.now())
    # db.session.add(a)
    # a = Admin(adminUserId='root',password='1')
    # a.add()
    # a = PhoneCode.query.filter_by(userId='root').first()
    # db.session.delete(a)
    # db.session.commit()
    pass


