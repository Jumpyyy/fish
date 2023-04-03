# """
#  Created by ldd on 2023.3.14
# """
# __author__ = 'ldd'
#
# from flask import Flask
#
#
# app = Flask(__name__)
# app.config.from_object('config')
# print(app.config['DEBUG'])
# print('id为', id(app), '的实例化')
#
# print(">>>>>>>>>>>>>>>>>>>start...")
# from app.web import book
# print(">>>>>>>>>>>>>>>>>>>end...")
#
# #
# # @app.route('/hello')
# # def hello():
# #     # status code 200,404,301
# #     # content-type http headers
# #     # content-type = text/html （默认）
# #     # Response
# #     headers = {
# #         # 'content-type': 'text/plain',
# #         'content-type': 'application/json',
# #         'location': 'https://www.baidu.com'
# #     }
# #     # response = make_response('<html></html>', 301)
# #     # response.headers = headers
# #     # return response
# #     return '<html></html>', 301, headers
#
# # app.add_url_rule('/hello', view_func=hello)
#
# if __name__ == '__main__':
#     # 生产环境： nginx+uwsgi
#     print('__main__app id: ', id(app))
#     app.run(host='0.0.0.0', debug=app.config['DEBUG'])
#
