"""
 Created by ldd on 2023/3/18.
"""

__author__ = 'ldd'

from sqlalchemy import Column, Integer, String, SmallInteger, ForeignKey
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.libs.enums import PendingStatus
from app.models.base import Base


class Drift(Base):
    """
        一次具体的交易信息
    """
    id = Column(Integer, primary_key=True)

    # 邮寄信息
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # 书籍信息
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 合理利用数据冗余
    # requester_id = Column(Integer, ForeignKey('user.id'))
    # requster = relationship('User')
    # gift_id = Column(Integer, ForeignKey('gift.id'))
    # gift = relationship('Gift')

    gift_id = Column(Integer)

    # 赠送者信息
    gifter_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    @property
    @hybrid_property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    @hybrid_property
    # status 为枚举类型 PendingStatus
    def pending(self, status):
        self._pending = status.value
