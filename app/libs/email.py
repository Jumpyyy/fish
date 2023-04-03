"""
 Created by ldd on 2023/3/18.
"""
import threading

from flask import current_app, render_template
from app import mail
from flask_mail import Message

__author__ = 'ldd'



def send_async_mail(app, msg):
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            raise e

def send_mail(to, subject, template, **kwargs):
    # message = Message('测试邮件', sender=current_app.config['MAIL_USERNAME'], body='Test',
    #                   recipients=[current_app.config['MAIL_USERNAME']])
    msg = Message('[鱼书]' + ' ' + subject, sender=current_app.config['MAIL_USERNAME'],
                      recipients=[to])
    msg.html = render_template(template, **kwargs)
    # 异步发送邮件
    # app_context = current_app.app_context()
    # thr = threading.Thread(target=send_async_mail, args=[app_context, msg])

    app = current_app._get_current_object()
    thr = threading.Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    # mail.send(msg)
