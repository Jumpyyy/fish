"""
 Created by ldd on 2023.3.14
"""

from app import create_app

app = create_app()



if __name__ == '__main__':
    # 生产环境： nginx+uwsgi
    # 本地调试环境，用的flask自带的web server。单进程单线程默认
    # threaded参数设为True后，单进程多线程。
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], threaded=False)

