from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, PasswordField, SelectField, TextAreaField, SubmitField, validators, \
    FileField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired,Length,EqualTo
from flask import flash,session
from model import Admin
from __init__ import db
from flask_login import login_user

class QueryListForm(FlaskForm):
    # 用户登陆表单
    userId = StringField(label='资金账号',
                         render_kw={
                             'placeholder': u'资金账号'
                         }
                         )

    userName = StringField(label='客户名称',
                           render_kw={
                               'placeholder': u'客户名称'
                           }
                           )

class AdminLoginForm(FlaskForm):
    # 用户登陆表单
    adminUserId = StringField(label='角色账号', validators=[DataRequired(message='资金账号不能为空')],
                         render_kw={
                             'placeholder': u'请输入角色账号'
                         }
                         )

    password = PasswordField(label='角色密码',
                             validators=[DataRequired(message='密码不能为空'), Length(1, 20, message='密码只能在6~20个字符之间')],
                             render_kw={
                                 'placeholder': u'请输入角色密码'
                             }
                             )

    submit = SubmitField(label='登录')
    # 验证UserId
    def validate_adminUserId(self, field):
        admin = Admin.query.filter_by(adminUserId=field.data).first()
        if not admin:
            raise validators.StopValidation(u'角色账户未找到')
        if not admin.check_password_hash(self.password.data):
            raise validators.StopValidation(u'密码不正确')
        login_user(admin)
        session['adminUserId'] = field.data
        session['tag'] = admin.tag


class ApplyForm(FlaskForm):
    # 用户申请界面
    zjs_1 = BooleanField(label='中金所1')
    nyzx_1 = BooleanField(label='能源中心1')
    nyzx_2 = BooleanField(label='能源中心2')
    sqs1 = BooleanField(label='上期所1')
    dss1 = BooleanField(label='大商所1')
    dss2 = BooleanField(label='大商所2')
    zss1 = BooleanField(label='郑商所1')
    zss2 = BooleanField(label='郑商所2')
    zjsbm = BooleanField(label='中金所编码')
    nyzxbm = BooleanField(label='能源中心编码')
    jyqx = BooleanField(label='交易权限')
    jyjl = BooleanField(label='交易记录')
    qtjyqx = BooleanField(label='其他交易权限')
    submit = SubmitField(label='通过')


class ChangePasswordForm(FlaskForm):
    # 用户注册表单
    adminUserId = StringField(label='角色账号',
                           validators=[DataRequired(message='姓名不能为空'), Length(2, 6, message='姓名只能在2~6个字符之间')],

                           )
    old_password = PasswordField(label='旧密码',
                             validators=[DataRequired(message='密码不能为空'), Length(1, 20, message='密码只能在6~20个字符之间')],
                             render_kw={
                                 'placeholder': u'请输入旧密码'
                             }
                             )
    password = PasswordField(label='密码',
                             validators=[DataRequired(message='密码不能为空'), Length(1, 20, message='密码只能在6~20个字符之间')],
                             render_kw={
                                 'placeholder': u'请输入新密码'
                             }
                             )
    confirm = PasswordField(label='确认密码',
                            validators=[EqualTo('password', message='两次密码不一致'),DataRequired(message='密码不能为空')],
                            render_kw={
                                'placeholder': u'请确认新密码'
                            }
                            )
    submit = SubmitField(label='确定',
                         render_kw={
                            'placeholder': u'确定'
    }
                         )
    # 验证UserId
    def validate_adminUserId(self, field):
        admin = Admin.query.filter_by(adminUserId=field.data).first()
        if not admin:
            raise validators.StopValidation(u'角色账户未找到')
        if not admin.check_password_hash(self.old_password.data):
            flash('密码不正确')
            raise validators.StopValidation(u'密码不正确')

        admin.password = self.password.data
        db.session.commit()

class RegisterForm(FlaskForm):
    # 用户注册表单
    adminUserId = StringField(label='角色账号',
                              validators=[DataRequired(message='姓名不能为空'), Length(2, 6, message='姓名只能在2~6个字符之间')],
                              render_kw={
                                  'placeholder': u'请输入角色账号',
                              }
                           )
    password = PasswordField(label='角色密码',
                             validators=[DataRequired(message='密码不能为空'), Length(2, 20, message='密码只能在6~20个字符之间')],
                             render_kw={
                                 'placeholder': u'请输入角色密码'
                             }
                             )
    jurisdiction = SelectMultipleField (label='权限分配',choices=[('0','权限一'),('1','权限二'),('2','权限三')],
                            render_kw={
                                'placeholder': u'请确认权限分配'
                            }
                            )
    submit = SubmitField(label='确定',
                         render_kw={
                            'placeholder': u'确定'
    }
                         )