"""
    Created by ldd on 2023/3/15 15:27
"""
from flask import Blueprint, render_template

# 蓝图 blueprint 初始化
# web = Blueprint('web', __name__, template_folder='templates', static_url_path='../static')
web = Blueprint('web', __name__)

@web.app_errorhandler(404)
def not_found(e):
    # AOP 思想
    # 把e 错误信息写入日志...
    return render_template('404.html'), 404


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
