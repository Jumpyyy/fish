
from . import web
from flask_login import login_required, current_user
from flask import current_app, flash, redirect, url_for, render_template

from ..libs.enums import PendingStatus
from ..models.base import db
from ..models.drift import Drift
from ..models.gift import Gift
from ..view_models.trade import TradeInfo, MyTrades


@web.route('/my/gifts')
@login_required
def my_gifts():
    gifts_of_mine = Gift.get_user_gifts(current_user.id)
    isbn_list = [my_gift.isbn for my_gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    # 获取到两个源数据gifts_of_mine、isbn_list后，还需要GiftsViewModel来封装
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    # 把isbn的校验看做是用户行为校验，未写在form层里，而是写在User里，方便此行为校验可被其他复用
    if current_user.can_save_to_list(isbn):
        # 事务
        # 回滚
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            #################################### （操作两个模型就是操作两个表，#号上面操作gift表，#号下面操作user表）
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            # ORM的方式保存模型
            db.session.add(gift)
            # db.session.commit()
    else:
        flash('这本书已存在你的赠送清单或者心愿清单中，请不要重复添加')
    return redirect(url_for('web.book_detail', isbn=isbn))





@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(uid=current_user.id, id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处在交易状态，请先前往鱼漂完成该交易')
    else:
        with db.auto_commit():
            gift.delete()
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
    return redirect(url_for('web.my_gifts'))


