from math import floor

from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedSerializer
from flask import current_app

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from flask_login import UserMixin

from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook


class User(UserMixin, Base):
    # __tablename__ = 'user1'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    # 鱼豆，可理解为虚拟货币积分
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    # flask_login插件要求定义的get_id函数, 还有几个默认的函数，可以直接继承UserMixin,
    # 如果此user模型里的id名不是id,比如是id1,则需写这个get_id来覆盖UserMixin的get_id
    # def get_id(self):
    #     return self.id

    def can_save_to_list(self, isbn):
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(isbn)
        if yushu_book.total == 0:
            return False
        # 不允许同一个用户同时！同时赠送多本相同的图书
        # 一个用户不可能同时成为同一本书的赠送者和索要者

        # 先查询这本图书是否已经存在于当前用户的赠送清单中，launched=False， 表示这本书还未赠送出去，不能上传同一本书加入心愿清单
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()
        # 这本图书是否存在用户的心愿清单中
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn, launched=False).first()

        # 合并下，判断条件为：这本图书既不在赠送清单中，也不在心愿清单中
        if gifting or wishing:
            return False
        return True


    def generate_token(self, expiration=600):
        s = TimedSerializer(current_app.config['SECRET_KEY'], expiration)
        # temp = s.dumps({'id': self.id})
        return 1

    @staticmethod
    def reset_password(token, new_password):
        # 通过token获取userId
        uid = 1
        with db.auto_commit():
            user = User.query.get(uid)
            if user:
                user.password = new_password
        return True

    def can_send_drift(self):
        if self.beans < 1:
            return False
        success_gift_count = Gift.query.filter_by(uid=self.id, launched=True).count()
        # success_wish_count = Wish.query.filter_by(uid=self.id, launched=True).count()
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id, pending=PendingStatus.Success).count()
        return True if floor(success_receive_count / 2) <= floor(success_gift_count) else False

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )


# 此函数属于user.py模块内的函数，不是User类里的。使用装饰器login_required时需要。
@login_manager.user_loader
def get_user(uid):
    # 根据主键查，不需要用filter_by， 用get就行
    return User.query.get(int(uid))