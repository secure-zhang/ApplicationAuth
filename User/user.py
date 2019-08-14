# -*- conding = utf-8 -*-

from __init__ import app,login_manager,db
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
    item = json.loads(request.data.decode('utf-8'))
    userId = item['userid'].strip()
    userName = item['username'].strip()

    user = User.query.filter_by(userId=userId,userName=userName).first()
    if user:
        # 若存在用户,生成验证码
        phone = user.phone
        code = random.randint(0, 999999)
        pc = PhoneCode(userId=userId,code=code)
        pc.add()
        return jsonify(status_code=200, msg="%s"%code)
    return jsonify(status_code=404, msg="账号或姓名错误")

# 申请表
@app.route('/user/apply',methods=['GET','POST'])
@login_required
def apply():
    form = ApplyForm()
    if form.validate_on_submit():
        userId = session['userId']
        cffex_c4 =form.cffex_c4.data
        ine_c3 =form.ine_c3.data
        ine_c4 =form.ine_c4.data
        shfe_c4 =form.shfe_c4.data
        dce_c3 = form.dce_c3.data
        dce_c4 =form.dce_c4.data
        czce_c3 =form.czce_c3.data
        czce_c4 =form.czce_c4.data
        cffex_code =form.cffex_code.data
        ine_code =form.ine_code.data
        company_auth =form.company_auth.data
        transact_record =form.transact_record.data
        outher_com_auth =form.outher_com_auth.data
        files =form.files.data
        try:
            data = UserData(userId=userId, cffex_c4=cffex_c4, ine_c3=ine_c3, ine_c4=ine_c4, shfe_c4=shfe_c4, dce_c3=dce_c3,
                          dce_c4=dce_c4, czce_c3=czce_c3, czce_c4=czce_c4, cffex_code=cffex_code, ine_code=ine_code, company_auth=company_auth, transact_record=transact_record,
                          outher_com_auth=outher_com_auth)
            tag2 = True
            if files:
                # 针对文件名称进行处理
                fileName = secure_filename(files.filename)
                # 获取二进制的文件
                # fileData = base64.b64encode(files.read())
                fileData = files.read()

                img = UserImage(userId=userId,fileName=fileName,fileData=fileData)
                tag2 = img.add()
            tag1 = data.add()
            if tag1 and tag2:
                user = User.query.filter_by(userId=userId).first()
                user.isData = True
                db.session.commit()

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