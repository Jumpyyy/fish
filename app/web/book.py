from flask import request, render_template, flash
from flask_login import current_user

from . import web
from app.libs.helper import is_isbn_or_key
from app.spider.yushu_book import YuShuBook
from ..forms.book import SearchForm
from ..models.gift import Gift
from ..models.user import User
from ..models.wish import Wish
from ..view_models.book import BookViewModel, BookCollection
import json

from ..view_models.trade import TradeInfo, _TradesCollection


@web.route('/book/search')  # 把视图函数注册到蓝图上
def search():
    """
        q: 普通关键字 isbn
        page
        ?q=金庸&page=1
    """
    # q = request.args['q']
    # page = request.args['page']
    # d = request.args.to_dict()  # request.args是一个unmutableDict 不可变的dict，可转dict
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
        else:
            yushu_book.search_by_keyword(q, page)

        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)
    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
    return render_template('search_result.html', books=books, form=form)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 是赠书人，则页面需切换为索要者。否则，默认页面，或者索要人页面，均显示谁有书。此逻辑有前端判断，传递has_in_gifts和has_in_wishes即可。
    # 下面这个if可以认为是业务逻辑，封装到User类里，类似于can_save_to_list（）函数
    if current_user.is_authenticated:
        # 默认查询status=1的，详见base里的MyQuery
        if Gift.query.filter_by(isbn=isbn, launched=False, uid=current_user.id).first():
            has_in_gifts = True
        if Wish.query.filter_by(isbn=isbn, launched=False, uid=current_user.id).first():
            has_in_wishes = True

    print('has_in_gifts=', has_in_gifts)
    print('has_in_wishes=', has_in_wishes)

    # 查询当前用户此本书籍的赠送清单、心愿清单
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html', book=book, wishes=trade_wishes_model, gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)



# @web.route('/book/<isbn>/detail')
def __book_detail(isbn):
    """
    自己实现，有小缺陷。另外封装的TradeCollection。
    :param isbn:
    :return:
    """
    has_in_gifts = False
    has_in_wishes = False

    # 取书籍详情数据
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    # 查询当前用户此本书籍的赠送清单、心愿清单
    gifts_collection = _TradesCollection()
    wishes_collection = _TradesCollection()
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # 当时为了不查第二次，用的uid的list判断，但是后续会有软删除业务，增加status判断，则必须重新查询。
    trade_gift_ids = [gift.uid for gift in trade_gifts]
    trade_wish_ids = [wish.uid for wish in trade_wishes]

    # 下面这个if可以认为是业务逻辑，封装到User类里，类似于can_save_to_list（）函数
    if current_user.is_authenticated:
        has_in_gifts = True if current_user.id in trade_gift_ids else False
        has_in_wishes = True if current_user.id in trade_wish_ids else False

    # 是赠书人，则页面需切换为索要者。否则，默认页面，或者索要人页面，均显示谁有书


    wishes_collection.fill(trade_wishes)
    gifts_collection.fill(trade_gifts)

    return render_template('book_detail.html', book=book, wishes=wishes_collection, gifts=gifts_collection,
                           has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)



@web.route('/test0')
def test_local():
    from app.libs.none_local import n
    print(n.v)
    n.v = 2
    print('---------------------')
    print(getattr(request, 'v', None))
    setattr(request, 'v', 2)
    print('----------------------')
    return ''


@web.route('/test')
def test():
    r = {
        'name': 'ldd',
        'age': 18
    }
    flash('A message flashed ldd')
    return render_template('test.html', data=r)
