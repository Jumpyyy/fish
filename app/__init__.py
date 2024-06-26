"""
    Created by ldd on 2023/3/15 15:29
"""
from flask import Flask
from flask_login import LoginManager
from app.models.base import db
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    # app = Flask(__name__, static_folder='cms/statics')
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或者注册'

    mail.init_app(app)
    return app


def register_blueprint(app):
    """
    把蓝图对象注册到app核心对象上
    这样最终实现视图函数在app核心对象上的注册
    """
    from app.web import web
    app.register_blueprint(web)
