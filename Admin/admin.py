# -*- conding = utf-8 -*-

from __init__ import app,login_manager
from flask_login import login_user, login_required,logout_user
from flask import render_template, request, redirect, url_for, session, jsonify,flash
from form import AdminLoginForm,QueryListForm,ApplyForm
from datetime import timedelta
import random,json,os
from model import Admin,User,Apply
# 创建 user 蓝图
from flask import Blueprint
admin = Blueprint('admin',__name__)

# 这个callback函数用于reload User object，根据session中存储的user id
@login_manager.user_loader
def load_admin_user(user_id):
    return Admin.query.get(int(user_id))

# 登出
@app.route('/logout')
def adminlogout():
    logout_user()
    session.pop('adminUserId',None)
    return redirect(url_for('index'))

# 登陆界面
@app.route('/admin/login',methods=['GET','POST'])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():

    #     系统判断柜台是否通过适当性测试，若已通过显示评级，若未通过，转到适当性链接
    #     用户信息持久化 30 分钟
        session['adminUserId'] = form.adminUserId.data
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('queryList'))
    return render_template('admin/adminLogin.html',form=form)



# 用户列表分页
@app.route('/admin/queryList',methods = ['GET', 'POST'])
@app.route('/queryList/<int:page>',methods = ['GET'])
def queryList(page=1):
    form = QueryListForm()
    if form.validate_on_submit():
        print(form.userId.data)
        print(form.userName.data)
        user = User.query.all()
    else:
        users = User.query.order_by(User.addTime.desc()).paginate(page,per_page=2,error_out=False)
    return render_template('admin/queryList.html', form=form,users=users)


# 用户详细信息

@app.route('/apply/<string:userId>',methods=['GET'])
def apply(userId):
    # 记录用户名称,用户id,文件名称 返回给前端
    item = {}
    user = User.query.filter_by(userId=userId).first()
    userName = user.userName
    item['userName']=userName
    item['userId']=userId
    form = ApplyForm()
    # 查询用户已提交的资料
    apply = Apply.query.filter_by(userId=userId).first()
    if not apply:
        item['fileName'] = False
        return render_template('admin/userApply.html', form=form, item=item)
    item['fileName']=apply.fileName
    if apply.zjs_1:
        form.zjs_1.checked='checked'
    if apply.nyzx_1:
        form.nyzx_1.checked='checked'
    if apply.nyzx_2:
        form.nyzx_2.checked='checked'
    if apply.sqs1:
        form.sqs1.checked='checked'
    if apply.dss1:
        form.dss1.checked='checked'
    if apply.dss2:
        form.dss2.checked='checked'
    if apply.zss1:
        form.zss1.checked='checked'
    if apply.zss2:
        form.zss2.checked='checked'
    if apply.zjsbm:
        form.zjsbm.checked='checked'
    if apply.nyzxbm:
        form.nyzxbm.checked='checked'
    if apply.jyqx:
        form.jyqx.checked='checked'
    if apply.jyjl:
        form.jyjl.checked='checked'
    if apply.qtjyqx:
        form.qtjyqx.checked='checked'
    return render_template('admin/userApply.html',form=form,item=item)

