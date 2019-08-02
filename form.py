from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField,TextAreaField,SubmitField,validators,FileField,RadioField
from wtforms.validators import DataRequired,Length,EqualTo
from flask import flash
from model import Application,PhoneCode
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
        user = Application.query.filter_by(userId=field.data).first()
        if not user:
            flash('账号或姓名错误请重新输入')
            raise validators.StopValidation(u'资金账号未找到')
        if user.userName != self.userName.data:
            flash('账号或姓名错误请重新输入')
            raise validators.StopValidation(u'姓名错误')









class ApplyForm(FlaskForm):
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
    files = FileField(label='文件')
    submit = SubmitField(label='下一步')




