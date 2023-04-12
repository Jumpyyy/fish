"""
 Created by ldd on 2023.3.14
"""
__author__ = 'ldd'

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:xxx@localhost:3306/fisher'
SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxx'

# Email 配置
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USE_TSL = False
MAIL_USERNAME = 'xxx@qq.com'
MAIL_PASSWORD = 'xxxxxx'
# MAIL_SUBJECT_PREFIX = '[鱼书]'
# MAIL_SENDER = '鱼书 <hello@yushu.im> hello ldd'