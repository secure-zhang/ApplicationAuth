from flask import Flask
from flask_wtf.csrf import CsrfProtect
from flask_sqlalchemy import SQLAlchemy
import os,pypyodbc
import redis

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
# app.debug = True

# 限制ip频繁请求
limiter = Limiter(
    app,
    key_func=get_remote_address,   #根据访问者的IP记录访问次数
    default_limits=["200 per day", "50 per hour"]  #默认限制，一天最多访问200次，一小时最多访问50次
)



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
login_manager.login_view = 'login'
login_manager.login_message = u""
login_manager.init_app(app=app)


# 指定数据库的链接信息
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pymssql://gt:server123!@#@172.0.10.59/GtPowerManage'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://zhang:zhang@94.191.80.61:3306/Application'
# 这个配置将来会被禁用,设置为True或者False可以解除警告信息,建议设置False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 配置sybase
sybase_db = pypyodbc.connect("DSN=sybase;UID=kstrader;PWD=kstrader")

# 配置redis
redis_db = redis.Redis(host='127.0.0.1',port=6379)#连接Redis

# 绑定蓝图
from user import user
app.register_blueprint(user, url_prefix='/user')

