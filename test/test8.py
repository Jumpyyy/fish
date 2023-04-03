"""
    Created by ldd on 2023/3/16 20:15
"""
"""
    Created by ldd on 2023/3/16 19:48
"""
import threading
import time

from werkzeug.local import LocalStack



my_stack = LocalStack()
my_stack.push(1)
print('in main thread after push, value is: ', str(my_stack.top))

def work():
    print('in new thread before push, value is: ', str(my_stack.top))
    my_stack.push(2)
    print('in new thread after push, value is: ', str(my_stack.top))

new_t = threading.Thread(target=work, name='ldd_thread')
new_t.start()
time.sleep(2)

print('finally,in main thread value is: ', str(my_stack.top))