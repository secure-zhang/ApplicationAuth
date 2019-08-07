# -*- conding = utf-8 -*-

from __init__ import app,login_manager
from flask_login import login_user, login_required,logout_user
from flask import render_template, request, redirect, url_for, session, jsonify,flash
from form import AdminLoginForm,QueryListForm
from datetime import timedelta
import random,json,os
from model import Admin,User
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
    return render_template('adminLogin.html',form=form)



# 用户列表分页
@app.route('/admin/queryList',methods = ['GET', 'POST'])
@app.route('/queryList/<int:page>',methods = ['GET'])
def queryList(page=1):
    form = QueryListForm()
    # if form.validate_on_submit():
    #     print(form.userId.data)
    #     print(form.userName.data)
    #     user = User.query.all()
    # else:
    users = User.query.order_by(User.addTime.desc()).paginate(page,per_page=2,error_out=False)
    return render_template('queryList.html', form=form,users=users)

@app.route('/admin/queryPage/',methods = ['GET', 'POST'])
def queryPage():
    item = request.args.to_dict()
    page = item.get('page','1')
    if page.isdigit():
        return redirect(url_for('queryList',page=int(page)))
    return jsonify(status_code=403, msg="请检查page")