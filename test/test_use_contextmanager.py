"""
 Created by ldd on 2023/3/18.
"""

__author__ = 'ldd'

# print('《且将生活一饮而尽》')

from contextlib import contextmanager

# 其实与@contextmanager没关系，只是想用下with，懒得去写__enter__和—__exit__方法，就用contextmanager偷懒了

@contextmanager
def book_mark():
    print('《', end='')
    yield
    print('》', end='')

with book_mark():
    print('且将生活一饮而尽', end='')




# @contextmanager
# def book_mark(name):
#     print('《')
#     yield book(name)
#     print('》')
#
# class book:
#     def __init__(self, name):
#         self.name = name
#
#     def __str__(self):
#         return self.name
#
# with book_mark('且将生活一饮而尽') as b:
#     print(b)