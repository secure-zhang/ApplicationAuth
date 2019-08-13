from __init__ import db
from _datetime import datetime
from flask_login._compat import unicode
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class Admin(UserMixin,db.Model):
    __tablename__ = 'Admin'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    adminUserId = db.Column(db.String(64),nullable=False)
    password_hash = db.Column(db.String(256),nullable=False)
    jurisdiction = db.Column(db.String(256),nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    tag = db.Column(db.Boolean(),nullable=False,default=False)
    def __str__(self):
        return 'User{adminUserId=%s}' % (self.adminUserId)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    #密码设置为hash
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    #验证密码
    def check_password_hash(self,password):
        return check_password_hash(self.password_hash,password)


    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except:
            return 0


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

class UserData(db.Model):
    __tablename__ = 'UserData'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),db.ForeignKey('User.userId'), nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    cffex_c4 = db.Column(db.Boolean(),nullable=False,default=False)
    ine_c3 = db.Column(db.Boolean(),nullable=False,default=False)
    ine_c4 = db.Column(db.Boolean(),nullable=False,default=False)
    shfe_c4 = db.Column(db.Boolean(),nullable=False,default=False)
    dce_c3 = db.Column(db.Boolean(),nullable=False,default=False)
    dce_c4 = db.Column(db.Boolean(),nullable=False,default=False)
    czce_c3 = db.Column(db.Boolean(),nullable=False,default=False)
    czce_c4 = db.Column(db.Boolean(),nullable=False,default=False)
    cffex_code = db.Column(db.Boolean(),nullable=False,default=False)
    ine_code = db.Column(db.Boolean(),nullable=False,default=False)
    company_auth = db.Column(db.Boolean(),nullable=False,default=False)
    transact_record = db.Column(db.Boolean(),nullable=False,default=False)
    outher_com_auth = db.Column(db.Boolean(),nullable=False,default=False)
    def __repr__(self):
        return '<User %r>' % (self.userId)
class UserImage(db.Model):
    __tablename__ = 'UserImage'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),db.ForeignKey('User.userId'), nullable=False)
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    fileName = db.Column(db.String(128))
    fileData = db.Column(db.LargeBinary(length=65536))
    def __repr__(self):
        return '<User %r>' % (self.userId)

if __name__ == '__main__':
    db.create_all()
#     a = Admin()
#     db.session.add(a)