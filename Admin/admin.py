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
@app.route('/admin/adminlogout')
def adminlogout():
    logout_user()
    session.pop('adminUserId',None)
    session.pop('tag',None)
    return redirect(url_for('adminLogin'))

# 登陆界面
@app.route('/admin/adminLogin',methods=['GET','POST'])
def adminLogin():
    form = AdminLoginForm()
    if form.validate_on_submit():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)
        return redirect(url_for('userList'))
    return render_template('admin/adminLogin.html',form=form)


# 用户列表分页
@app.route('/admin/userList',methods = ['GET'])
@app.route('/userList/<int:page>',methods = ['GET'])
@login_required
def userList(page=1):
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
    return render_template('admin/userList.html', form=form,users=users)



# 用户详细信息
@app.route('/userData/<string:userId>',methods=['GET'])
@login_required
def userData(userId):
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
        return render_template('admin/userData.html', form=form, item=item)

    if image.fileName:
        item['fileName']=image.fileName
        item['fileData']= re.match("b'(.*?)'",str(image.fileData)).group(1)
    if data.cffex_c4:
        form.cffex_c4.checked='checked'
    if data.ine_c3:
        form.ine_c3.checked='checked'
    if data.ine_c4:
        form.ine_c4.checked='checked'
    if data.shfe_c4:
        form.shfe_c4.checked='checked'
    if data.dce_c3:
        form.dce_c3.checked='checked'
    if data.dce_c4:
        form.dce_c4.checked='checked'
    if data.czce_c3:
        form.czce_c3.checked='checked'
    if data.czce_c4:
        form.czce_c4.checked='checked'
    if data.cffex_code:
        form.cffex_code.checked='checked'
    if data.ine_code:
        form.ine_code.checked='checked'
    if data.company_auth:
        form.company_auth.checked='checked'
    if data.transact_record:
        form.transact_record.checked='checked'
    if data.outher_com_auth:
        form.outher_com_auth.checked='checked'
    return render_template('admin/userData.html',form=form,item=item,base64=base64)


# 用户已处理： 当前端点击通过跳转该视图函数，判断角色是否有权限更改用户的操作
@app.route('/admin/userAdopt',methods=['GET','POST'])
@login_required
def userAdopt():
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
@app.route('/admin/userImgDel',methods=['GET','POST'])
@login_required
def userImgDel():
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

# 修改密码
@app.route('/admin/adminPassword',methods=['GET','POST'])
@login_required
def adminPassword():
    item = {}
    form = ChangePasswordForm()
    form.adminUserId.render_kw = {
        'value':session['adminUserId'],
        'readonly':'readonly'
    }
    if form.validate_on_submit():
        flash('修改成功')
    return render_template('admin/adminPassword.html',form=form,item=item)


# 注册角色
@app.route('/admin/adminRegister',methods=['GET','POST'])
@login_required
def adminRegister():
    # 判断是否为超级管理员
    if not session['tag']:
        abort(404)

    item = {}
    form = RegisterForm()
    if form.validate_on_submit():
        adminUserId = form.adminUserId.data
        password = form.password.data
        jurisdiction = json.dumps({'data':form.jurisdiction.data})
        admin = Admin.query.filter_by(adminUserId=adminUserId).first()
        if admin:
            admin.password = password
            admin.jurisdiction = jurisdiction
        else:
            a = Admin(adminUserId=adminUserId,password=password,jurisdiction=jurisdiction)
            db.session.add(a)
        db.session.commit()
        flash('角色: %s 已重置'%adminUserId)
    return render_template('admin/adminRegister.html',form=form,item=item)
