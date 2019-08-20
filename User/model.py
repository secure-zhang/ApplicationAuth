from __init__ import db
from _datetime import datetime
from flask_login._compat import unicode


class User(db.Model):
    __tablename__ = 'User'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer(),primary_key=True,autoincrement=True)
    userId = db.Column(db.String(64),nullable=False,unique=True)
    userName = db.Column(db.String(64),nullable=False)
    userClass = db.Column(db.String(64),nullable=False) # 用户类
    userGrade = db.Column(db.Integer(),nullable=False)  # 用户评级
    phone = db.Column(db.String(11),nullable=False)
    isHandle = db.Column(db.Integer(),nullable=False,default=2)
    isData = db.Column(db.Boolean(),nullable=False,default=False)
    handleName = db.Column(db.String(11),nullable=False,default='无')
    addTime = db.Column(db.DateTime(), nullable=False, default=datetime.now())
    updateTime = db.Column(db.DateTime())
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
    fileData = db.Column(db.Text())
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

if __name__ == '__main__':
    # db.create_all()
    db.session.add(User(userId='root7',userName='root7',phone='176',userClass='SH',userGrade=1))
    db.session.add(User(userId='root8',userName='root8',phone='176',userClass='SH',userGrade=2))
    db.session.add(User(userId='root1',userName='root1',phone='176',userClass='SH',userGrade=3))
    db.session.add(User(userId='root2',userName='root2',phone='176',userClass='SH',userGrade=4))
    db.session.add(User(userId='root3',userName='root3',phone='176',userClass='SH',userGrade=5))
    db.session.add(User(userId='root4',userName='root4',phone='176',userClass='SH',userGrade=3))
    db.session.add(User(userId='root5',userName='root5',phone='176',userClass='SH',userGrade=4))
    db.session.add(User(userId='root6',userName='root6',phone='176',userClass='SH',userGrade=5))
    db.session.commit()

    # print(a)
    # a = Admin(adminUserId='root',password='1')
    # a.add()
    # a = PhoneCode.query.filter_by(userId='root').first()
    # db.session.delete(a)
    # db.session.commit()
    pass


