from datetime import datetime

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy.query import Query
from sqlalchemy import Column, SmallInteger, Integer
from contextlib import contextmanager


class SQLAlchemy(_SQLAlchemy):
    """
    直接定义一个方法,肯定是可以的. 但是 可以考虑到所有的model ,都会对数据库 进行 写入操作.
    因此 可以写在base_model 里面比较合适, 这样只要从base 继承的model ,都会有 auto_commit 这个方法了.
    """
    @contextmanager
    def auto_commit(self):
        try:
            yield
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

class MyQuery(Query):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super().filter_by(**kwargs)

db = SQLAlchemy(query_class=MyQuery)


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    # python的动态赋值
    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            return datetime.fromtimestamp(self.create_time)
        else:
            return None