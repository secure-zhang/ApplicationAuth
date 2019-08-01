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
