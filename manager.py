# -*- conding = utf-8 -*-

from __init__ import app,login_user, login_required,login_manager,logout_user
from flask import render_template

@app.route('/',methods=['GET','POST'])
def test():
    return render_template('test.html')

# 异常处理
@app.errorhandler(400)
def not_found(e):
    return render_template('test.html')

if __name__ == '__main__':
    app.run()