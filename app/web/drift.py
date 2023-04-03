from sqlalchemy import or_, desc

from . import web
from flask_login import login_required, current_user
from flask import render_template, flash, redirect, url_for, request

from ..forms.book import DriftForm
from ..libs.email import send_mail
from ..libs.enums import PendingStatus
from ..models.base import db
from ..models.drift import Drift
from ..models.gift import Gift
from ..models.user import User
from ..models.wish import Wish
from ..view_models.book import BookViewModel
from ..view_models.drift import DriftCollection


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('这本书是你自己的， 不能向自己索要书籍噢')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    if not current_user.can_send_drift():
        flash('您的鱼豆不足')
        return render_template('not_enough_beans.html', beans=current_user.beans)

    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        # 将数据保存到drift表中，记得扣鱼豆
        save_drift(form, current_gift)
        # email 短信提醒
        send_mail(current_gift.user.email, '有人想要一本书', 'email/get_gift.html',
                  wisher=current_user, gift=current_gift)
        return redirect(url_for('web.pending'))

    gifter = current_gift.user.summary
    return render_template('drift.html', gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    drifts = Drift.query.filter(or_(Drift.requester_id == current_user.id, Drift.gifter_id == current_user.id))\
        .order_by(desc(Drift.create_time)).all()

    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.datas)


@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        drift.pending = PendingStatus.Reject
        user = User.query.get_or_404(drift.requester_id)
        user.beans += 1
    return redirect(url_for('web.pending'))



@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    # 横向越权
    # uid:1  did:1
    # uid:2  did:2
    with db.auto_commit():
        dirft = Drift.query.filter_by(requester_id=current_user.id, id=did).first_or_404()
        dirft.pending = PendingStatus.Redraw
        current_user.beans += 1
    #     从pending页面跳转到pending页面，最好是前端用ajax去写。
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
def mailed_drift(did):
    with db.auto_commit():
        dirft = Drift.query.filter_by(gifter_id=current_user.id, id=did).first_or_404()
        dirft.pending = PendingStatus.Success
        current_user.beans += 2
    #   gift和wish表的launched需改为已赠送或已心愿达成
        gift = Gift.query.filter_by(id=dirft.gift_id).first_or_404()
        gift.launched = True
        Wish.query.filter_by(uid=dirft.requester_id, isbn=dirft.isbn,
                                    launched=False).update({Wish.launched: True})
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    with db.auto_commit():
        drift = Drift()
        # drift.message = drift_form.message.data
        # drift_form表单里的字段和drift里的名称一致的话，可以直接populate_obj方法
        drift_form.populate_obj(drift)

        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        # 需判断下beans >= 1
        current_user.beans -= 1
        db.session.add(drift)
