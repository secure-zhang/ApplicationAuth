# -*- conding = utf-8 -*-


from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField,SubmitField,validators,FileField
from wtforms.validators import DataRequired,Length
from flask import flash
from model import User,PhoneCode
from flask_login import login_user
from __init__ import db


class LoginForm(FlaskForm):
    # 用户登陆表单
    userId = StringField(label='资金账号', validators=[DataRequired(message='资金账号不能为空')],
                         render_kw={
                             'placeholder': u'资金账号'
                         }
                         )

    userName = StringField(label='姓名（自然人）',
                           validators=[DataRequired(message='姓名不能为空'), Length(2, 6, message='姓名只能在2~6个字符之间')],
                           render_kw={
                               'placeholder': u'姓名（自然人）'
                           }
                           )

    code = StringField(label='验证码',validators=[DataRequired(message='验证码不能为空')],
                       render_kw={
                           'placeholder': u'验证码'
                       }
                       )
    read_old = BooleanField(label='已阅读框',validators=[DataRequired()])

    submit = SubmitField(label='下一步')
    # 验证是资金账号否存在
    def validate_userId(self, field):

        if not self.userId.data or not self.userName.data or not self.code.data or not self.read_old.data:
            flash('请正确填写信息')
            raise validators.StopValidation(u'请正确填写信息')

        user = User.query.filter_by(userId=field.data,userName=self.userName.data.strip()).first()
        if not user:
            flash('账号或姓名错误请重新输入')
            raise validators.StopValidation(u'资金账号未找到')

        pc = PhoneCode.query.filter_by(userId=field.data,code=self.code.data.strip()).order_by(PhoneCode.addTime.desc()).first()
        if not pc:
            flash('验证码错误')
            raise validators.StopValidation(u'验证码错误')

        # 验证成功后删除验证码
        db.session.delete(pc)
        db.session.commit()

        # 用户登陆，每次访问链接都通过此函数进行验证
        login_user(user)




class ApplyForm(FlaskForm):
    # 用户申请界面
    cffex_c4 = BooleanField(label='中金所1')
    ine_c3 = BooleanField(label='能源中心1')
    ine_c4 = BooleanField(label='能源中心2')
    shfe_c4 = BooleanField(label='上期所1')
    dce_c3 = BooleanField(label='大商所1')
    dce_c4 = BooleanField(label='大商所2')
    czce_c3 = BooleanField(label='郑商所1')
    czce_c4 = BooleanField(label='郑商所2')
    cffex_code = BooleanField(label='中金所编码')
    ine_code = BooleanField(label='能源中心编码')
    company_auth = BooleanField(label='交易权限')
    transact_record = BooleanField(label='交易记录')
    outher_com_auth = BooleanField(label='其他交易权限')
    files = FileField(label='文件',validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(label='下一步')





