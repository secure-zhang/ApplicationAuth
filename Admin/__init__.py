from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
# app = Flask(__name__)

# app.debug = True

app.config["SECRET_KEY"] = os.urandom(24)
app.secret_key = os.urandom(24)
# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)


# 用户登录模块
from flask_login import LoginManager

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'adminLogin'
login_manager.login_message = u""
login_manager.init_app(app=app)


# 指定数据库的链接信息
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://gt:server123!@#@172.0.10.59/GtPowerManage'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://zhang:zhang@94.191.80.61:3306/Application'

# 这个配置将来会被禁用,设置为True或者False可以解除警告信息,建议设置False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from admin import admin
app.register_blueprint(admin, url_prefix='/admin')

