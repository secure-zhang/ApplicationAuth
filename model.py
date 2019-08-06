from __init__ import db
from _datetime import datetime
from flask_login._compat import unicode
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),nullable=False,unique=True)
    userName = db.Column(db.String(64),nullable=False)
    phone = db.Column(db.String(11),nullable=False)
    isHandle = db.Column(db.Boolean(),nullable=False,default=False)
    handleName = db.Column(db.String(11),nullable=False,default='暂无')
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

class Apply(db.Model):
    __tablename__ = 'Apply'
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
    fileName = db.Column(db.String(128))
    fileData = db.Column(db.LargeBinary(length=65536))
    def add(self):
        try:
            db.session.add(self)
            db.session.commit()
            return 1
        except Exception as e:
            print(e)
            return 0
    def __repr__(self):
        return '<userId %r>' % (self.userId)


class Admin(UserMixin,db.Model):
    __tablename__ = 'Admin'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    adminUserId = db.Column(db.String(64),nullable=False)
    password_hash = db.Column(db.String(256),nullable=False)

    def __str__(self):
        return 'User{adminUserId=%s,password=%s,}' % (self.adminUserId, self.password,)

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

    def __repr__(self):
        return '<User %r>' % (self.name)

if __name__ == '__main__':
    db.create_all()
    # a = Application(userId='root',userName='张泽睿',phone='17635035787',addTime=datetime.now())
    # db.session.add(a)
    # a = Admin(adminUserId='root',password='1')
    # a.add()
    # a = PhoneCode.query.filter_by(userId='root').first()
    # db.session.delete(a)
    # db.session.commit()
    pass


