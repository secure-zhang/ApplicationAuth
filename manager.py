# -*- conding = utf-8 -*-

from __init__ import app,login_user, login_required,login_manager,logout_user
from flask import render_template,request,redirect,url_for,session
from form import LoginForm,ApplyForm
from datetime import timedelta


@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/explain',methods=['GET','POST'])
def explain():
    return render_template('explain.html')

@app.route('/success',methods=['GET','POST'])
def success():
    return render_template('success.html')

@app.route('/apply',methods=['GET','POST'])
def apply():
    form = ApplyForm()
    if form.validate_on_submit():
        return redirect(url_for('explain'))
    return render_template('apply.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        # 系统判断柜台是否通过适当性测试，若已通过显示评级，若未通过，转到适当性链接
        tag = True
        if tag:
            return redirect(url_for('apply'))
        return redirect(location='http://114.251.192.185:8080/clients/register/start')
    return render_template('login.html',form=form)

if __name__ == '__main__':
    app.run('192.168.1.3',5000)