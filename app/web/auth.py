"""
 Created by ldd on 2023/3/18.
"""

from . import web
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user
from ..forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from ..models.base import db
from ..models.user import User

__author__ = 'ldd'


@web.route('/register', methods=['GET', 'POST'])
def register():
    # request.args获取url里？后面的参数，request.form获取请求提交的表单数据
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # # ORM的方式保存模型(用with，增加事务回滚）
        with db.auto_commit():
            user = User()
            # 如果需要预处理下password，可以利用getter setter方法，在User类里
            # user.password = generate_password_hash(form.password.data)
            user.set_attrs(form.data)
            db.session.add(user)
            # db.session.commit()    # 用with写法自动commit
        # 重定向后一定要记得return
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # 通过flask_login包里的login_user，间接地将用户票据写入cookie中
            # login_user需要入参user里的userId代表用户的身份信息，所以user需要定义一个固定的get_id
            login_user(user)
            # 访问login_required的请求后会被引导到登录页面，比如访问gifts： http://192.168.10.2:5000/login?next=/my/gifts
            # 登录后再返回原页面，需要next参数
            next = request.args.get('next')
            # 防止重定向攻击
            if not next or not next.startswith('/') :
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_user = form.email.data
            user = User.query.filter_by(email=account_user).first_or_404()
            # 如果用户邮箱查询的用户存在，则系统发送一封重置密码的邮件,不存在会自动跳到404(AOP)
            from app.libs.email import send_mail
            send_mail(form.email.data, '重置你的密码', 'email/reset_password.html', user=user,
                      token=user.generate_token())
            flash('一封邮件已发送到邮箱' + account_user + ', 请及时查收')
            # try:
            #     send_mail(form.email.data, '重置你的密码', 'email/reset_password.html', user=user,
            #               token=user.generate_token())
            #     flash('一封邮件已发送到邮箱' + account_user + ', 请及时查收')
            # except:
            #     flash('一封邮件已发送到邮箱' + account_user + '失败,请重试!')
    return render_template('auth/forget_password_request.html', form=form)



@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('你的密码已更新，请使用新密码登录')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    pass


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))
