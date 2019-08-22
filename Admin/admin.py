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
from _datetime import datetime

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


# 用户列表ajax分页
@app.route('/admin/userList',methods = ['GET'])
@app.route('/userList',methods = ['GET'])
@login_required
def userList(page=1,userId='',userName=''):
    form = QueryListForm()
    data = request.args
    jurisdiction = tuple(session['jurisdiction'])
    users = User.query.filter(User.isData==True,User.userClass.in_(jurisdiction)).order_by(User.addTime.desc()).paginate(page, per_page=10, error_out=False)

    item = {}
    # 如果是通过submit 提交则从url中获取数据
    if data:
        userId = data.get('userId').strip()
        userName = data.get('userName').strip()
        page = int(data.get('page','1').strip())
        # 将表单中的数据赋值给表单
        if userId:
            form.userId.render_kw = {
                'value': userId
            }
        if userName:
            form.userName.render_kw = {
                'value': userName
            }
        # 若提交的时候没用参数则查全部数据按照添加时间进行排序,否则按照字段进行模糊查询
        if not userId and not userName:
            users = User.query.filter(User.isData==True,User.userClass.in_(jurisdiction)).order_by(User.addTime.desc()).paginate(page, per_page=10, error_out=False)
        if  userId or  userName:
            users = User.query.filter(User.isData==True,User.userClass.in_(jurisdiction),User.userId.like("%" + userId + "%"), User.userName.like("%" + userName + "%")).order_by(User.addTime.desc()).paginate(page, per_page=10, error_out=False)
    item['userId'] = userId
    item['userName'] = userName
    return render_template('admin/userList.html', form=form,users=users,item=item)


# 用户详细信息
@app.route('/userData/<string:userId>',methods=['GET'])
@login_required
def userData(userId):
    # 记录用户名称,用户id,文件名称 返回给前端
    item = {'img':{}}
    jurisdiction = tuple(session['jurisdiction'])
    user = User.query.filter_by(userId=userId).first()
    # 防止管理员获取无权限用户信息
    if not user:
        return redirect(url_for('userList'))

    if user.userClass not in jurisdiction:
        return redirect(url_for('userList'))
    userName = user.userName
    isHandle = user.isHandle
    item['userName']=userName
    item['userId']=userId
    form = ApplyForm()
    # 若用户已被处理则不可被操作
    item['isHandle']=isHandle
    if isHandle == 1:
            form.cffex_c4.render_kw['disabled']='disabled'
            form.ine_c3.render_kw['disabled']='disabled'
            form.ine_c4.render_kw['disabled']='disabled'
            form.shfe_c4.render_kw['disabled']='disabled'
            form.dce_c3.render_kw['disabled']='disabled'
            form.dce_c4.render_kw['disabled']='disabled'
            form.czce_c3.render_kw['disabled']='disabled'
            form.czce_c4.render_kw['disabled']='disabled'
            form.cffex_code.render_kw['disabled']='disabled'
            form.ine_code.render_kw['disabled']='disabled'
            form.company_auth.render_kw['disabled']='disabled'
            form.transact_record.render_kw['disabled']='disabled'
            form.outher_com_auth.render_kw['disabled']='disabled'
    else:
        form.cffex_c4.render_kw['disabled'] = False
        form.ine_c3.render_kw['disabled'] = False
        form.ine_c4.render_kw['disabled'] = False
        form.shfe_c4.render_kw['disabled'] = False
        form.dce_c3.render_kw['disabled'] = False
        form.dce_c4.render_kw['disabled'] = False
        form.czce_c3.render_kw['disabled'] = False
        form.czce_c4.render_kw['disabled'] = False
        form.cffex_code.render_kw['disabled'] = False
        form.ine_code.render_kw['disabled'] = False
        form.company_auth.render_kw['disabled'] = False
        form.transact_record.render_kw['disabled'] = False
        form.outher_com_auth.render_kw['disabled'] = False
    # 查询用户已提交的资料
    data = UserData.query.filter_by(userId=userId).order_by(UserData.addTime.desc()).first()
    if data:
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

    image = UserImage.query.filter_by(userId=userId).all()
    if image:
        for i in image:
            item['img'][i.fileName]=i.fileData
    else:
        item['img'] = ''
    return render_template('admin/userData.html',form=form,item=item,base64=base64)


# 用户已处理： 当前端点击通过跳转该视图函数，判断角色是否有权限更改用户的操作
@app.route('/admin/userAdopt',methods=['GET','POST'])
@login_required
def userAdopt():

    if request.method == 'POST':
            # 获取被修改用户id与管理员名称
            adminUserId = session['adminUserId']
            item = json.loads(request.data.decode('utf-8'))
            userId = item['userId'].strip()

            # 将用户修改为已被处理
            jurisdiction = tuple(session['jurisdiction'])
            user = User.query.filter(User.userId == userId).first()
            # 防止管理员获取无权限用户信息
            if not user:
                return redirect(url_for('userList'))

            if user.userClass not in jurisdiction:
                return redirect(url_for('userList'))

            user.isHandle = True
            user.handleName = adminUserId
            user.updateTime = datetime.now()
            db.session.commit()
            return jsonify(status_code=200, msg="发送成功")
    abort(404)

# 删除图片
@app.route('/admin/userImgDel',methods=['GET','POST'])
@login_required
def userImgDel():
    if request.method == 'POST':
        try:
            item = json.loads(request.data.decode('utf-8'))
            userId = item['userId'].strip()
            fileName = item['fileName'].strip()
            result = UserImage.query.filter_by(userId=userId,fileName=fileName).first()
            db.session.delete(result)
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
