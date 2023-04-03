"""
 Created by 七月 on 2018/1/26.
 微信公众号：林间有风
"""

from . import web



__author__ = '七月'


from flask import render_template
from ..models.gift import Gift
from ..view_models.book import BookViewModel


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    print(len(recent_gifts))
    # 要返回的事书籍信息，即用BookViewModel, 需要gift转book。可以把book当做gift的属性
    # Model层的数据 --> View的数据
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)

@web.route('/personal')
def personal_center():
    pass
