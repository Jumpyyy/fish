"""
    Created by ldd on 2023/3/17 18:30
"""
class A:
    def __init__(self):
        self.total = 0
        self.books = []

    def fill(self, data):
        if data:
            self.total = 1
            self.books.append(data)


d = {
    "author": [
        "蔡智恒"
    ],
    "binding": "平装",
    "category": "小说",
    "id": 1780,
    "isbn": "9787501524044"
}

def test():
    a = A()
    a.fill(d)
    print(a.__dict__)

test()