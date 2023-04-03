# print("book start..")
# from fisher import app
# print("book end..")
#
# from helper import is_isbn_or_key
# from yushu_book import YuShuBook
#
# print('book import yushu_book>>>')
# @app.route('/book/search/<q>/<page>')
# def search(q, page):
#     """
#         q: 普通关键字 isbn
#         page
#     """
#     isbn_or_key = is_isbn_or_key(q)
#     if isbn_or_key == 'isbn':
#         result = YuShuBook.search_by_isbn(q)
#     else:
#         result = YuShuBook.search_by_keyword(q)
#     return result
#
# print('注册view function， appid:', id(app))