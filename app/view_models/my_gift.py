"""
 Created by ldd on 2023/3/18.
"""
from collections import namedtuple

__author__ = 'ldd'

# 已被MyTrades替代
# from app.view_models.book import BookViewModel
#
# # MyGift = namedtuple('MyGift', ['id', 'book', 'wishes_count'])
#
# class MyGifts:
#     def __init__(self, gifts_of_mine, wish_count_list):
#         self.gifts = []
#         self.__gifts_of_mine = gifts_of_mine
#         self.__wish_count_list = wish_count_list
#
#         self.gifts = self.__parse()
#
#     def __parse(self):
#         return [self.__matching(gift) for gift in self.__gifts_of_mine]
#         # temp_gifts = []
#         # for gift in self.__gifts_of_mine:
#         #     my_gift = self.__matching(gift)
#         #     temp_gifts.append(my_gift)
#         # return temp_gifts
#
#     def __matching(self, gift):
#         count = 0
#         for wish_count in self.__wish_count_list:
#             if wish_count['isbn'] == gift.isbn:
#                 count = wish_count['count']
#         # 后续讲序列化，用字典，暂时不用MyGift类
#         # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
#         # return my_gift
#         r = {
#             'id': gift.id,
#             'book': BookViewModel(gift.book),
#             'wishes_count': count
#         }
#         return r



