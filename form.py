from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, PasswordField,TextAreaField,SubmitField,validators,FileField,RadioField
from wtforms.validators import DataRequired,Length,EqualTo
from flask import flash,session
from model import User,PhoneCode,Admin
from __init__ import db,login_user


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

        user = User.query.filter_by(userId=field.data).first()
        if not user:
            flash('账号或姓名错误请重新输入')
            raise validators.StopValidation(u'资金账号未找到')
        if user.userName != self.userName.data.strip() :
            flash('账号或姓名错误请重新输入')
            raise validators.StopValidation(u'姓名错误')
        pc = PhoneCode.query.filter_by(userId=field.data).order_by(PhoneCode.addTime.desc()).first()
        if not pc:
            # 判断验证码是否存在
            flash('请刷新重试')
            raise validators.StopValidation(u'请刷新重试')

        # 判断验证码是否正确
        if self.code.data != pc.code :
            flash('验证码错误')
            raise validators.StopValidation(u'验证码错误')

        # 验证成功后删除验证码
        db.session.delete(pc)
        db.session.commit()

        # 用户登陆，每次访问链接都通过此函数进行验证
        login_user(user)




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
    files = FileField(label='文件',validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField(label='下一步')





