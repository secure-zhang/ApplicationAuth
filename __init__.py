from flask import Flask
from flask_wtf.csrf import CsrfProtect
import os
app = Flask(__name__)

app.debug = True
app.config["SECRET_KEY"] = "rootzhang"
app.secret_key = os.urandom(24)
# csrf protection
csrf = CsrfProtect()
csrf.init_app(app)

# 用户登录模块
from flask_login import login_user, login_required
from flask_login import LoginManager, current_user
from flask_login import logout_user

# use login manager to manage session
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = u""
login_manager.init_app(app=app)
