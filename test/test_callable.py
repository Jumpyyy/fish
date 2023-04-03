"""
 Created by ldd on 2023/3/18.
"""

__author__ = 'ldd'

class A():
    # def go(self):
    #     return object()
    def __call__(self):
        return object()

class B():
    def run(self):
        return object()

def func():
    return object()


def main(callable):
    callable()
    # 我想在main中调用传入的参数，得到一个object对象
    # a.go()
    # b.run()
    # func()
    # ...
    # 所以，A类里实现callable，即可像调用函数一样调用A()


if __name__ == '__main__':
    main(A())
    # main(B())