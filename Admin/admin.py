# -*- conding = utf-8 -*-

from __init__ import app,login_manager,db
from flask_login import  login_required,logout_user
from flask import render_template, request, redirect, url_for, session, jsonify,flash,abort
from form import AdminLoginForm,QueryListForm,ApplyForm,ChangePasswordForm,RegisterForm
from datetime import timedelta
import json,re
from model import Admin,User,UserData,UserImage
# 创建 user 蓝图
from flask import Blueprint
admin = Blueprint('admin',__name__)
import base64

@login_manager.user_loader
def load_admin_user(user_id):
    return Admin.query.get(int(user_id))

# 登出
@app.route('/admin/logout')
def adminlogout():
    logout_user()
    session.pop('adminUserId',None)
    return redirect(url_for('index'))

# 登陆界面
@app.route('/admin/login',methods=['GET','POST'])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        session['adminUserId'] = form.adminUserId.data
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('queryList'))
    return render_template('admin/adminLogin.html',form=form)


# 用户列表分页
@app.route('/admin/queryList',methods = ['GET'])
@app.route('/queryList/<int:page>',methods = ['GET'])
@login_required
def queryList(page=1):
    form = QueryListForm()
    data = request.args
    users = User.query.order_by(User.addTime.desc()).paginate(page, per_page=5, error_out=False)
    if data:
        userId = data.get('userId')
        userName = data.get('userName')
        if not userId and not userName:
            users = User.query.order_by(User.addTime.desc()).paginate(page, per_page=5, error_out=False)
        if userId or userName:
            users = User.query.filter(User.userId.like("%" + userId + "%"), User.userName.like("%" + userName + "%")).paginate(page, per_page=5, error_out=False)
    return render_template('admin/queryList.html', form=form,users=users)



# 用户详细信息
@app.route('/apply/<string:userId>',methods=['GET'])
@login_required
def apply(userId):
    # 记录用户名称,用户id,文件名称 返回给前端
    item = {}
    user = User.query.filter_by(userId=userId).first()
    userName = user.userName
    item['userName']=userName
    item['userId']=userId
    form = ApplyForm()

    # 查询用户已提交的资料
    data = UserData.query.filter_by(userId=userId).first()
    image = UserImage.query.filter_by(userId=userId).first()
    if not image:
        item['fileName'] = False
        return render_template('admin/userApply.html', form=form, item=item)

    if image.fileName:
        item['fileName']=image.fileName
        item['fileData']= re.match("b'(.*?)'",str(image.fileData)).group(1)
    if data.zjs_1:
        form.zjs_1.checked='checked'
    if data.nyzx_1:
        form.nyzx_1.checked='checked'
    if data.nyzx_2:
        form.nyzx_2.checked='checked'
    if data.sqs1:
        form.sqs1.checked='checked'
    if data.dss1:
        form.dss1.checked='checked'
    if data.dss2:
        form.dss2.checked='checked'
    if data.zss1:
        form.zss1.checked='checked'
    if data.zss2:
        form.zss2.checked='checked'
    if data.zjsbm:
        form.zjsbm.checked='checked'
    if data.nyzxbm:
        form.nyzxbm.checked='checked'
    if data.jyqx:
        form.jyqx.checked='checked'
    if data.jyjl:
        form.jyjl.checked='checked'
    if data.qtjyqx:
        form.qtjyqx.checked='checked'
    return render_template('admin/userApply.html',form=form,item=item,base64=base64)


# 用户已处理： 当前端点击通过跳转该视图函数，判断角色是否有权限更改用户的操作
@app.route('/admin/adopt',methods=['GET','POST'])
@login_required
def adopt():
    if request.method == 'POST':
        # 获取被修改用户id与管理员名称
            adminUserId = session['adminUserId']
            item = json.loads(request.data)
            userId = item['userId'].strip()

            # 将用户修改为已被处理
            result = User.query.filter(User.userId == userId).first()
            result.isHandle = True
            result.handleName = adminUserId
            db.session.commit()

            return jsonify(status_code=200, msg="发送成功")

    abort(404)

# 删除图片
@app.route('/admin/deleteImg',methods=['GET','POST'])
@login_required
def deleteImg():
    if request.method == 'POST':
        try:
            item = json.loads(request.data)
            userId = item['userId'].strip()
            result = UserImage.query.filter_by(userId=userId).first()
            result.fileName = None
            result.fileData = None
            db.session.commit()
            return jsonify(status_code=200, msg="发送成功")
        except:
            abort(404)
    abort(404)


@app.route('/admin/changePassword',methods=['GET','POST'])
@login_required
def changePassword():
    item = {}
    form = ChangePasswordForm()
    form.adminUserId.render_kw = {
        'value':session['adminUserId'],
        'readonly':'readonly'
    }
    if form.validate_on_submit():
        flash('修改成功')
    return render_template('admin/changePassword.html',form=form,item=item)

@app.route('/admin/administrator',methods=['GET','POST'])
# @login_required
def administrator():
    item = {}
    form = RegisterForm()
    return render_template('admin/Administrator.html',form=form,item=item)
