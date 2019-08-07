from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, PasswordField,TextAreaField,SubmitField,validators,FileField,RadioField
from wtforms.validators import DataRequired,Length,EqualTo
from flask import flash,session
from model import Admin
from __init__ import db
from flask_login import login_user

class QueryListForm(FlaskForm):
    # 用户登陆表单
    userId = StringField(label='资金账号', validators=[DataRequired(message='资金账号不能为空')],
                         render_kw={
                             'placeholder': u'资金账号'
                         }
                         )

    userName = StringField(label='客户名称',
                           validators=[DataRequired(message='姓名不能为空'), Length(2, 6, message='姓名只能在2~6个字符之间')],
                           render_kw={
                               'placeholder': u'客户名称'
                           }
                           )


    submit = SubmitField(label='查询')

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
    # 验证邮箱是否存在
    def validate_adminUserId(self, field):
        admin = Admin.query.filter_by(adminUserId=field.data).first()
        if not admin:
            raise validators.StopValidation(u'角色账户未找到')
    # 验证密码
    def validate_password(self, field):
        admin = Admin.query.filter_by(adminUserId=self.adminUserId.data).first()
        if admin:
            if not admin.check_password_hash(field.data):
                raise validators.StopValidation(u'密码不正确')