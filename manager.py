# -*- conding = utf-8 -*-

from __init__ import app,login_user, login_required,login_manager,logout_user
from flask import render_template, request, redirect, url_for, session, jsonify,flash
from form import LoginForm,ApplyForm,explainForm
from datetime import timedelta
import random,json
from model import Application,PhoneCode,Apply


# 这个callback函数用于reload User object，根据session中存储的user id
# 用户登陆
@login_manager.user_loader
def load_user(user_id):
    return Application.query.get(int(user_id))

# 登出
@app.route('/logout')
def logout():
    logout_user()
    session.pop('username',None)
    session.pop('user_id',None)
    return redirect(url_for('index'))
@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/test',methods=['GET','POST'])
def test():
    form = ApplyForm()
    print(request.files)
    return render_template('test.html',form=form)


@app.route('/sendCode',methods=['POST'])
def sendCode():
    # 判断客户提交账号与名称是否正确，若正确则发送验证码
    item = json.loads(request.data)
    userId = item['userid'].strip()
    userName = item['username'].strip()

    user = Application.query.filter_by(userId=userId,userName=userName).first()
    if user:
        # 若存在用户,生成验证码
        phone = user.phone
        code = random.randint(0, 999999)
        pc = PhoneCode(userId=userId,code=code)
        pc.add()
        return jsonify(status_code=200, msg="发送成功")

    return jsonify(status_code=201, msg="账号或姓名错误请重新输入")


@app.route('/explain',methods=['GET','POST'])
@login_required
def explain():
    form = explainForm()
    return render_template('explain.html',form=form)

@app.route('/success',methods=['GET','POST'])
def success():
    logout()
    return render_template('success.html')
@app.route('/apply',methods=['GET','POST'])
@login_required
def apply():
    form = ApplyForm()
    if form.validate_on_submit():
        userId = session['userId']
        zjs_1 =form.zjs_1.data
        nyzx_1 =form.nyzx_1.data
        nyzx_2 =form.nyzx_2.data
        sqs1 =form.sqs1.data
        dss1 = form.dss1.data
        dss2 =form.dss2.data
        zss1 =form.zss1.data
        zss2 =form.zss2.data
        zjsbm =form.zjsbm.data
        nyzxbm =form.nyzxbm.data
        jyqx =form.jyqx.data
        jyjl =form.jyjl.data
        qtjyqx =form.qtjyqx.data
        files =form.files.data
        ap = Apply(userId=userId,zjs_1=zjs_1,nyzx_1=nyzx_1,nyzx_2=nyzx_2,sqs1=sqs1,dss1=dss1,
                  dss2=dss2,zss1=zss1,zss2=zss2,zjsbm=zjsbm,nyzxbm=nyzxbm,jyqx=jyqx,jyjl=jyjl,
                  qtjyqx=qtjyqx,files=files)
        tag = ap.add()
        if  tag:
            flash(u'上传成功')
            return redirect(url_for('explain'))
        else:
            flash(u'上传失败')
    return render_template('apply.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 系统判断柜台是否通过适当性测试，若已通过显示评级，若未通过，转到适当性链接
        tag = True
        if tag:
            # 用户信息持久化 30 分钟
            session['userId'] = form.userId.data
            session['userName'] = form.userName.data
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect(url_for('apply'))
        return redirect(location='http://114.251.192.185:8080/clients/register/start')
    return render_template('login.html',form=form)

# 异常处理
@app.errorhandler(400)
def not_found(e):
    return render_template('test.html')

if __name__ == '__main__':
    app.run()