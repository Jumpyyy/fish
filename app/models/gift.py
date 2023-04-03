from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, desc, func
from sqlalchemy.orm import relationship
from flask import current_app
from collections import namedtuple


from app.spider.yushu_book import YuShuBook

EachGiftWishCount = namedtuple('EachGiftWishCount', ['count', 'isbn'])


class Gift(Base):
    id = Column(Integer, primary_key=True)
    # Gift.query时，user也会被查到
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))
    # 未关联book表，而是通过isbn去查，如后面的book属性。
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))
    isbn = Column(String(15), nullable=False)
    # 是否已被赠送，默认值为未被赠送
    launched = Column(Boolean, default=False)

    # 通过当前gift的isbn可以获取到book（YuShuBook的search_by_isbn），把book当做gift的一个属性，方便后续获取
    @property
    def book(self):
        yushu_book = YuShuBook()
        yushu_book.search_by_isbn(self.isbn)
        return yushu_book.first

    def delete(self):
        self.status = 0

    def is_yourself_gift(self, uid):
        return True if self.uid == uid else False

    # 需求：完成最近上传，即最近的gifts. 在gift表里查询，即写在gift Model层里
    # 对象代表一个礼物， 具体
    # 类代表礼物这个事物，它是抽象，不是具体的“一个”。（该方法如果是实例方法则不合适，故用@classmethod）
    @classmethod
    def recent(cls):
        """
        完成三个：取最新（按时间排序）的30条数据，且去重
        """
        # 链式调用
        # 主体 Query
        # 子函数  filter_by  group_by...
        # first() all()
        recent_gifts = Gift.query.filter_by(
            launched=False).group_by(
            Gift.isbn).order_by(
            desc(Gift.create_time)).limit(
            current_app.config['RECENT_BOOK_COUNT']).all()
        return recent_gifts



    @classmethod
    def get_user_gifts(cls, uid):
        gifts = Gift.query.filter_by(uid=uid, launched=False).order_by(
            desc(Gift.create_time)).all()
        return gifts

    @classmethod
    def get_wish_counts(cls, isbn_list):
        from app.models.wish import Wish
        # 根据传入的一组isbn检索，到Wish表计算某个礼物的wish心愿数量
        # db.session  条件表达式，不同于Gift.query.filter_by里的都是查询参数
        # 这个只是用了in_查询，我们需要的事一组数量，需要group_by后，分组查询统计wish.id数量
        # db.session.query(Wish).filter(Wish.launched == False,
        #                               Wish.isbn.in_(isbn_list),
        #                               Wish.status == 1).all()

        # count_list = [(2, '9787506337496'), (1, '9787501942657')]
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(Wish.launched == False,
                                  Wish.isbn.in_(isbn_list),
                                  Wish.status == 1).group_by(Wish.isbn).all()

        # 方式一: 转为类：用named_tuple处理count_list
        # count_list = [EachGiftWishCount(w[0], w[1]) for w in count_list]
        # 方式二：转为dict
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list

    # @property
    # def wishes_count(self):
    #     # my_gifts.html的13 36行，遍历gifts,根据每个礼物的isbn去wish表中查询这个书籍相关的心愿，缺点是循环遍历查询数据库
    #     wishes = Wish.query.filter_by(launched=False, isbn=self.isbn).all()
    #     return len(wishes)