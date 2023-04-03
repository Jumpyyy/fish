"""
    Created by ldd on 2023/3/16 13:03
"""

# from flask import Flask, current_app
#
# app = Flask(__name__)
#
# with app.app_context():
#     a = current_app
#     print(a)
#     d = current_app.config['DEBUG']

# a = current_app
# d = current_app.config['DEBUG']

class MyResource:
    def __enter__(self):
        print('connect to resource...')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print('process exception')
        else:
            print('no exception')
        print('exit resource...')
        return True

    def query(self):
        print('query data')

with MyResource() as resource:
    resource.query()