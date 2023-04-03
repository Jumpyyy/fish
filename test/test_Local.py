"""
    Created by ldd on 2023/3/16 19:48
"""
import threading
import time

from werkzeug.local import Local

# 原理 字典
# werkzeug local Local 字典
# L 线程隔离的对象
# t1.L.a   t2.L.a

my_obj = Local()
my_obj.b = 1

def work():
    my_obj.b = 2
    print('in new thread b is: ', str(my_obj.b))

new_t = threading.Thread(target=work, name='ldd_thread')
new_t.start()
time.sleep(2)

print('in main thread b is: ', str(my_obj.b))

