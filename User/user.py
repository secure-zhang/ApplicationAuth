# -*- conding = utf-8 -*-

from __init__ import app,login_manager
from flask_login import  login_required,logout_user
from flask import render_template, request, redirect, url_for, session, jsonify,flash,abort
from form import LoginForm,ApplyForm
from datetime import timedelta
import random,json
from model import User,PhoneCode,UserData,UserImage

# 创建 user 蓝图
from flask import Blueprint
from werkzeug.utils import secure_filename
import base64

user = Blueprint('user',__name__)


# 基础知识学习提示函
@app.route('/user/index',methods=['GET'])
def index():
    return render_template('user/index.html')


# 这个callback函数用于reload User object
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# 登陆界面
@app.route('/user/login',methods=['GET','POST'])
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
    return render_template('user/login.html',form=form)

# 登出
@app.route('/user/logout')
def logout():
    logout_user()
    session.pop('userName',None)
    session.pop('userId',None)
    return redirect(url_for('index'))


# 获取验证码
@app.route('/user/sendCode',methods=['POST'])
def sendCode():
    # 判断客户提交账号与名称是否正确，若正确则发送验证码
    item = json.loads(request.data)
    userId = item['userid'].strip()
    userName = item['username'].strip()

    user = User.query.filter_by(userId=userId,userName=userName).first()
    if user:
        # 若存在用户,生成验证码
        phone = user.phone
        code = random.randint(0, 999999)
        pc = PhoneCode(userId=userId,code=code)
        pc.add()
        return jsonify(status_code=200, msg="发送成功 code%s"%code)
    return jsonify(status_code=404, msg="账号或姓名错误")

# 申请表
@app.route('/user/apply',methods=['GET','POST'])
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
        try:
            data = UserData(userId=userId, zjs_1=zjs_1, nyzx_1=nyzx_1, nyzx_2=nyzx_2, sqs1=sqs1, dss1=dss1,
                          dss2=dss2, zss1=zss1, zss2=zss2, zjsbm=zjsbm, nyzxbm=nyzxbm, jyqx=jyqx, jyjl=jyjl,
                          qtjyqx=qtjyqx)
            tag2 = True
            if files:
                # 针对文件名称进行处理
                fileName = secure_filename(files.filename)
                # 获取二进制的文件
                fileData =base64.b64encode(files.read())

                img = UserImage(userId=userId,fileName=fileName,fileData=fileData)
                tag2 = img.add()
            tag1 = data.add()
            if tag1 and tag2:
                flash(u'上传成功')
                return redirect(url_for('explain'))
        except:
            flash(u'上传失败：请检查文件')
            # abort(404)
    return render_template('user/apply.html',form=form)

# 风险说明书
@app.route('/user/explain',methods=['GET'])
@login_required
def explain():
    return render_template('user/explain.html')

# 关闭界面
@app.route('/user/success',methods=['GET','POST'])
def success():
    logout()
    return render_template('user/success.html')