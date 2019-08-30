# -*- conding = utf-8 -*-

from __init__ import app,login_manager,db,limiter
from flask_login import  login_required,logout_user
from flask import render_template, request, redirect, url_for, session, jsonify,flash,abort,Response
from form import LoginForm,ApplyForm
from datetime import timedelta
import random,json
from model import User,PhoneCode,UserData,UserImage
import uuid,re,requests
from config import Sybase,RedisHelper

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
        try:
            # 判断用户是否已提交申请
            user = User.query.filter_by(userId=form.userId.data.strip()).first()
            if user.isData:
                return redirect(url_for('success'))

            # 在session存储用户信息
            session['userId'] = user.userId
            session['userName'] = user.userName
            session['userGrade'] = user.userGrade

            # 用户信息持久化 30 分钟
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=30)
            return redirect(url_for('apply'))
        except:
            abort(Response('login error'))
    return render_template('user/login.html',form=form)

# 登出
@app.route('/user/logout')
def logout():
    logout_user()
    session.pop('userName',None)
    session.pop('userId',None)
    session.pop('userGrade',None)
    return redirect(url_for('index'))

 # 设置ip限制
@limiter.limit( "3 per hour")
# 获取验证码
@app.route('/user/sendCode',methods=['POST'])
def sendCode():
    # 获取ajax传送的数据
    item = json.loads(request.data.decode('utf-8'))
    userId = item['userid'].strip()
    userName = item['username'].strip()

    # 验证是否存在且手机号格式是否正确
    s = Sybase()
    phone = s.cust_whole(userId,userName)
    if phone:
        ret = re.match(r"^1[3-9]\d{9}$", phone)
        if not ret:
            return jsonify(status_code=202, msg="手机号格式错误,联系客服修改,客服电话：400-6678-656")
        else:
            phone = ret.group()
    else:
        return jsonify(status_code=202, msg="用户信息存在错误,请联系客服,客服电话：400-6678-656")

    # 验证客户类是否存在
    userClass = s.cust_basic(userId)
    if not userClass:
        return jsonify(status_code=202, msg="未查询到客户类,联系客服修改,客服电话：400-6678-656")

    # 验证是否通过显示评级，若未通过，转到适当性链接
    userGrade = s.cust_appropriate_assessment(userId)
    if not userGrade:
        return jsonify(status_code=301, msg="请进行适当性测试")

    # 将用户数据添加到数据库
    user = User.query.filter_by(userId=userId,userName=userName).first()
    if not user:
        User(userId=userId, userName=userName, phone=phone, userClass=userClass,userGrade=userGrade).add()


    # 随机生成验证码
    code = random.randint(0, 999999)

    # 记录验证码
    redis_db = RedisHelper()
    tag = redis_db.add_code(userId,code)

    # 发送验证码
    if tag:
        code_msg = ('验证码:%s' % code).encode('gb2312')
        code_msg = str(code_msg).replace(r'\x', r'%')[2:-1]
        url = 'http://www.139000.com/send/gsend.asp?name=%b9%da%cd%a8%c6%da%bb%f5&pwd=gtqh0037&dst={dst}&msg={msg}'.format(
            dst='17635035787', msg=code_msg)
        # requests.get(url)
        return jsonify(status_code=200, msg="验证码发送成功%s" % code)
    else:
        return jsonify(status_code=202, msg="验证码记录失败")


# 申请表
@app.route('/user/apply',methods=['GET','POST'])
@login_required
def apply():
    try:
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

            # 通过评级防止记录用户通过html修改页面恶意串改的数据
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

            # 记录数据
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
            else:
                redirect(url_for('apply'))

        return render_template('user/apply.html',form=form)
    except:
        abort(Response('apply error '))

@app.route('/user/send_img',methods=['POST'])
@login_required
def send_img():
    try:
        item = json.loads(request.data.decode('utf-8'))
        img_base64 = item['base64']
        userId = session['userId']
        uuid_str = uuid.uuid4()
        fileName = '%s-%s.png' % (userId,uuid_str)
        img = UserImage(userId=userId, fileName=fileName, fileData=img_base64)
        img.add()
        return jsonify(status_code=200)
    except:
        return jsonify(status_code=404)



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
    session.pop('userGrade',None)
    logout_user()
    return render_template('user/success.html')