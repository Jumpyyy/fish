"""
 Created by 七月 on 2018/1/26.
 微信公众号：林间有风
"""
from flask import flash, redirect, url_for, render_template
from flask_login import current_user, login_required

from . import web


__author__ = '七月'

from ..libs.email import send_mail

from ..libs.enums import PendingStatus

from ..models.base import db
from ..models.drift import Drift
from ..models.gift import Gift
from ..models.wish import Wish
from ..view_models.trade import MyTrades


@web.route('/my/wish')
@login_required
def my_wish():
    wishes_of_mine = Wish.get_user_wishes(current_user.id)
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    # 获取到两个源数据wishes_of_mine、count_list后，还需要GiftsViewModel来封装

    view_model = MyTrades(wishes_of_mine, gift_count_list)
    # print(len(view_model))
    # for t in view_model.trades:
    #     print(t)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已存在你的赠送清单或者心愿清单中，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.filter_by(id=wid, launched=False).first_or_404()
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn, launched=False).first()
    if not gift:
        flash('你还没有上传此书， '
              '请点击“加入到赠送清单”添加此书。添加前，请确保自己可以赠送此书')
    else:
        send_mail(wish.user.email, '有人想送你一本书', 'email/satisify_wish.html', wish=wish, gift=gift)
        flash('已向他/她发送了一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))

@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))


