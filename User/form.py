# -*- conding = utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,SubmitField,validators,FileField
from wtforms.validators import DataRequired,Length
from flask import flash
from model import User,PhoneCode
from flask_login import login_user
from config import RedisHelper


class LoginForm(FlaskForm):
    # 用户登陆表单
    userId = StringField(label='资金账号',
                         validators=[DataRequired(message='资金账号不能为空')],
                         render_kw={
                             'placeholder': u'资金账号',
                         }
                         )

    userName = StringField(label='姓名（自然人）',
                           validators=[DataRequired(message='姓名不能为空')],
                           render_kw={
                               'placeholder': u'姓名（自然人）'
                           }
                           )

    code = StringField(label='验证码',
                       validators=[DataRequired(message='验证码不能为空'), Length(2, 6, message='验证码错误')],
                       render_kw={
                           'placeholder': u'验证码'
                       }
                       )
    read_old = BooleanField(label='已阅读框',validators=[DataRequired()])

    submit = SubmitField(label='下一步')
    def validate_userId(self, field):
        # 是否为空
        if not self.userId.data or not self.userName.data or not self.code.data or not self.read_old.data:
            flash('请正确填写信息')
            raise validators.StopValidation(u'请正确填写信息')

        # 用户是否存在
        userId = field.data
        userName = self.userName.data.strip()
        code = self.code.data.strip()
        user = User.query.filter_by(userId=userId,userName=userName).first()
        if not user:
            flash('账号或姓名错误请重新输入')
            raise validators.StopValidation(u'资金账号未找到')

        # 验证码是否有效
        redis_db = RedisHelper()
        redis_code = redis_db.get_code(userId)
        if not redis_code or redis_code != code.strip():
            flash('验证码错误')
            raise validators.StopValidation(u'验证码错误')


        # 验证成功后删除验证码
        tag = redis_db.delete_code(userId)
        if not tag:
            flash('验证码清除失败')
            raise validators.StopValidation(u'验证码清除失败')

        # 用户登陆
        login_user(user)




class ApplyForm(FlaskForm):
    # 用户申请界面
    cffex_c4 = BooleanField(label='中金所1',
                            render_kw={
                               'disabled': 'disabled'
                           })
    ine_c3 = BooleanField(label='能源中心1',
                          render_kw={
                              'disabled': 'disabled'
                          })
    ine_c4 = BooleanField(label='能源中心2',
                          render_kw={
                              'disabled': 'disabled'
                          })
    shfe_c4 = BooleanField(label='上期所1',
                          render_kw={
                              'disabled': 'disabled'
                          })
    dce_c3 = BooleanField(label='大商所1',
                          render_kw={
                              'disabled': 'disabled'
                          })
    dce_c4 = BooleanField(label='大商所2',
                          render_kw={
                              'disabled': 'disabled'
                          })
    czce_c3 = BooleanField(label='郑商所1',
                          render_kw={
                              'disabled': 'disabled'
                          })
    czce_c4 = BooleanField(label='郑商所2',
                          render_kw={
                              'disabled': 'disabled'
                          })
    cffex_code = BooleanField(label='中金所编码')
    ine_code = BooleanField(label='能源中心编码')
    company_auth = BooleanField(label='交易权限')
    transact_record = BooleanField(label='交易记录')
    outher_com_auth = BooleanField(label='其他交易权限')
    submit = SubmitField(label='确认')





