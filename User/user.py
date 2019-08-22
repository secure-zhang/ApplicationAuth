# -*- conding = utf-8 -*-

from __init__ import app,login_manager,db
from flask_login import  login_required,logout_user
from flask import render_template, request, redirect, url_for, session, jsonify,flash,abort
from form import LoginForm,ApplyForm
from datetime import timedelta
import random,json
from model import User,PhoneCode,UserData,UserImage
import uuid
from config import Sybase

# 创建 user 蓝图
from flask import Blueprint
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
        user = User.query.filter_by(userId=form.userId.data.strip()).first()
        if user.isData:
            return redirect(url_for('success'))

        # 用户信息持久化 30 分钟
        session['userId'] = user.userId
        session['userName'] = user.userName
        session['userGrade'] = user.userGrade

        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('apply'))
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
    # 从sybase获取用户数据并写入数据库
    s = Sybase()
    phone = s.cust_whole(userId,userName)
    userClass = s.cust_basic(userId)
    userGrade = s.cust_appropriate_assessment(userId)
    print(userId,userName,phone, userClass, userGrade)
    if phone and userClass :
        if not userGrade:
            # 系统判断柜台是否通过适当性测试，若已通过显示评级，若未通过，转到适当性链接
            return jsonify(status_code=404, msg="请进行适当性测试")
        # 判断，手机号是否正确,

        # 将用户数据添加到数据库
        user = User.query.filter_by(userId=userId,userName=userName).first()
        if not user:
            User(userId=userId, userName=userName, phone=phone, userClass=userClass,userGrade=userGrade).add()
        # 生成验证码
        code = random.randint(0, 999999)
        pc = PhoneCode(userId=userId,phone=phone,code=code)
        pc.add()

        return jsonify(status_code=200, msg="%s"%code)

    return jsonify(status_code=404, msg="账号或姓名错误,请联系客服,客服电话：400-6678-656")

# 申请表
@app.route('/user/apply',methods=['GET','POST'])
@login_required
def apply():
    form = ApplyForm()
    # 判断用户的评测级别并按级别显示可选申请
    userGrade = session['userGrade']
    if userGrade >= 3:
        form.ine_c3.render_kw['disabled']=False
        form.czce_c3.render_kw['disabled']=False
        form.dce_c3.render_kw['disabled']=False

    if userGrade >= 4:
        form.cffex_c4.render_kw['disabled']=False
        form.ine_c4.render_kw['disabled']=False
        form.shfe_c4.render_kw['disabled']=False
        form.dce_c4.render_kw['disabled']=False
        form.czce_c4.render_kw['disabled']=False

    if form.validate_on_submit():
        userId = session['userId']

        # 防止用户通过html修改页面恶意串改数据
        if userGrade <= 3:
            ine_c3 =form.ine_c3.data
            dce_c3 = form.dce_c3.data
            czce_c3 =form.czce_c3.data
        else:
            ine_c3 =False
            dce_c3 = False
            czce_c3 =False
        if userGrade <= 4:
            cffex_c4 =form.cffex_c4.data
            ine_c4 =form.ine_c4.data
            shfe_c4 =form.shfe_c4.data
            dce_c4 =form.dce_c4.data
            czce_c4 =form.czce_c4.data
        else:
            cffex_c4 = False
            ine_c4 = False
            shfe_c4 = False
            dce_c4 = False
            czce_c4 = False

        cffex_code = form.cffex_code.data
        ine_code =form.ine_code.data
        company_auth =form.company_auth.data
        transact_record =form.transact_record.data
        outher_com_auth =form.outher_com_auth.data
        data = UserData(userId=userId, cffex_c4=cffex_c4, ine_c3=ine_c3, ine_c4=ine_c4, shfe_c4=shfe_c4, dce_c3=dce_c3,
                      dce_c4=dce_c4, czce_c3=czce_c3, czce_c4=czce_c4, cffex_code=cffex_code, ine_code=ine_code, company_auth=company_auth, transact_record=transact_record,
                      outher_com_auth=outher_com_auth)

        tag1 = data.add()
        if tag1:
            userId = session['userId']
            user = User.query.filter_by(userId=userId).first()
            user.isData = True
            db.session.commit()
            return redirect(url_for('explain'))

    return render_template('user/apply.html',form=form)

@app.route('/user/send_img',methods=['POST'])
@login_required
def send_img():
    item = json.loads(request.data.decode('utf-8'))
    img_base64 = item['base64']
    userId = session['userId']
    uuid_str = uuid.uuid4()
    fileName = '%s-%s.png' % (userId,uuid_str)
    img = UserImage(userId=userId, fileName=fileName, fileData=img_base64)
    img.add()
    return jsonify(status_code=200)


# 风险说明书
@app.route('/user/explain',methods=['GET'])
@app.route('/user/explain/<int:tag>',methods=['GET'])
@login_required
def explain(tag=0):
    if tag == 1:
        return render_template('user/Agreement/ComplianceLetterHonestyCommitment.html')
    if tag == 2:
        return render_template('user/Agreement/FuturesTradingRiskInstructions.html')
    else:
        return render_template('user/explain.html')

# 关闭界面
@app.route('/user/success',methods=['GET','POST'])
@login_required
def success():

    session.pop('userName',None)
    session.pop('userId',None)
    logout_user()
    return render_template('user/success.html')