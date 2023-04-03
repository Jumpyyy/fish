"""
    Created by ldd on 2023/3/17 16:01
"""
class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.author = book['author']
        self.publisher = book['publisher']
        self.pages = book['pages']
        self.price = book['price']
        self.image = book['image']
        self.summary = book['summary']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [''.join(self.author), self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book_data) for book_data in yushu_book.books]




class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['books'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'books': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['books'] = [cls.__cut_book_data(book_data) for book_data in data['books']]
        return returned

    @staticmethod
    def __cut_book_data(data):
        book = {
            'title': data['title'],
            'author': '、'.join(data['author']),
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'price': data['price'],
            'image': data['image'],
            'summary': data['summary'] or ''
        }
        return book