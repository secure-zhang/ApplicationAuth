from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, BooleanField, PasswordField, SelectField, TextAreaField, SubmitField, validators, \
    FileField, RadioField, SelectMultipleField
from wtforms.validators import DataRequired,Length,EqualTo
from flask import flash,session
from model import Admin
from __init__ import db
from flask_login import login_user
import json
class QueryListForm(FlaskForm):
    # 用户表单
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
        session['adminUserId'] = admin.adminUserId
        session['jurisdiction'] = json.loads(admin.jurisdiction)['data']
        session['tag'] = admin.tag


class ApplyForm(FlaskForm):
    # 用户申请界面
    cffex_c4 = BooleanField(label='中金所1',
                            render_kw={
                               'disabled': False
                           })
    ine_c3 = BooleanField(label='能源中心1',
                          render_kw={
                              'disabled': False
                          })
    ine_c4 = BooleanField(label='能源中心2',
                          render_kw={
                              'disabled': False
                          })
    shfe_c4 = BooleanField(label='上期所1',
                          render_kw={
                              'disabled': False
                          })
    dce_c3 = BooleanField(label='大商所1',
                          render_kw={
                              'disabled': False
                          })
    dce_c4 = BooleanField(label='大商所2',
                          render_kw={
                              'disabled': False
                          })
    czce_c3 = BooleanField(label='郑商所1',
                          render_kw={
                              'disabled': False
                          })
    czce_c4 = BooleanField(label='郑商所2',
                          render_kw={
                              'disabled': False
                          })
    cffex_code = BooleanField(label='中金所编码',
                          render_kw={
                              'disabled': False
                          })
    ine_code = BooleanField(label='能源中心编码',
                          render_kw={
                              'disabled': False
                          })
    company_auth = BooleanField(label='交易权限',
                          render_kw={
                              'disabled': False
                          })
    transact_record = BooleanField(label='交易记录',
                          render_kw={
                              'disabled': False
                          })
    outher_com_auth = BooleanField(label='其他交易权限',
                          render_kw={
                              'disabled': False
                          })
    submit = SubmitField(label='确认')

class ChangePasswordForm(FlaskForm):
    # 修改密码
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
    jurisdiction = SelectMultipleField (label='权限分配',choices=[
        ('SH', '上海'),('GY', '贵阳'),
        ('QD', '青岛'),('ZB', '总部2'),('ZZ', '郑州'),
        ('DG', '金融业务部'),('DL', '大连'),('BJ', '北京'),
        ('CB', '深圳分公司1'),('QH', '秦皇岛'),('BC', '资管一'),
        ('ZT', '投四'),('BS', '中化集团'),('BY', '中化上下'),
        ('TJ', '天津'),('WH', '武汉'),('CS', '长沙'),
        ('CD', '成都'),('NT', '南通'),('SZ', '深圳'),
        ('GX', '深圳分公司'),('BB', '金融产业部'),('BK', '上门'),
        ('BW', '业务一部'),('GT', '高管业务'),('GZ', '深圳分公司2'),
        ('JN', '境外中介'),('JS', '北京事业三部'),('JY', '交易'),
        ('NN', '北京事业二部'),('SW', '商务中心'),('TT', '事业部1'),
        ('XT', '外贸信托'),('XY', '金融拓展部'),('YG', '员工'),
        ('YH', '北京事业一部'),('YZ', '投一'),('ZG', '资管'),

    ],render_kw={
                    'placeholder': u'请确认权限分配'
                }
                )
    submit = SubmitField(label='确定',
                         render_kw={
                            'placeholder': u'确定'
    }
                         )