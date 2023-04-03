"""
 Created by ldd on 2023/3/18.
"""

__author__ = 'ldd'

class MyResource:
    # def __enter__(self):
    #     print('connect to resource...')
    #     return self
    #
    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     print('exit resource...')
    #     return True

    def query(self):
        print('query data')

# with MyResource() as resource:
#     resource.query()

# 如果MyResource类不是一个上下文管理的类，比如未实现__enter__和__exit__方法，那么用contextmanager可以将此类包装为一个上下文管理的

from contextlib import contextmanager

@contextmanager
def make_myresource():
    print('connect to resource...')
    yield MyResource()
    print('exit resource...')

# yield 生成器
with make_myresource() as r:
    r.query()