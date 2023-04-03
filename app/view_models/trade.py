"""
 Created by ldd on 2023/3/18.
"""

__author__ = 'ldd'

from app.models.user import User
from app.view_models.book import BookViewModel


#自己实现的TradeInfo
class _TradeViewModel:
    def __init__(self, single):
        self.id = single.uid
        self.user_name = single.user.nickname
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        self.time = time


class _TradesCollection:
    def __init__(self):
        self.total = 0
        self.trades = []

    def fill(self, trades):
        self.total = len(trades)
        self.trades = [_TradeViewModel(single) for single in trades]


class TradeInfo:
    def __init__(self, goods):
        self.total = 0
        self.trades = []
        self.__parse(goods)

    def __parse(self, goods):
        self.total = len(goods)
        self.trades = [self.__map_to_trade(single) for single in goods]

    def __map_to_trade(self, single):
        if single.create_datetime:
            time = single.create_datetime.strftime('%Y-%m-%d')
        else:
            time = '未知'
        return dict(
            user_name=single.user.nickname,
            time=time,
            id=single.id
        )

# MyGifts or MyWishes
class MyTrades:
    def __init__(self, trades_of_mine, trade_count_list):
        self.trades = []
        self.__trades_of_mine = trades_of_mine
        self.__trade_count_list = trade_count_list

        self.trades = self.__parse()

    def __parse(self):
        return [self.__matching(trade) for trade in self.__trades_of_mine]

    def __matching(self, trade):
        count = 0
        for trade_count in self.__trade_count_list:
            if trade_count['isbn'] == trade.isbn:
                count = trade_count['count']
        # 后续讲序列化，用字典，暂时不用MyGift类
        # my_gift = MyGift(gift.id, BookViewModel(gift.book), count)
        # return my_gift
        r = {
            'id': trade.id,
            'book': BookViewModel(trade.book),
            'wishes_count': count
        }
        return r
