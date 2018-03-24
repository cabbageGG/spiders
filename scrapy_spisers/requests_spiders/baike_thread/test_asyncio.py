#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/2 11:12'

#协程真的没什么用，一定要用在异步io中，才能体现出作用。
#因为协程，还是单线程。仍然需要等待io。而多进程的消费者生产者模式的阻塞，基本可以忽略。

import asyncio
import time

now = lambda: time.time()

# async def hello_sleep(s):
#     time.sleep(s)

# async def do_some_work(x):
#     print('Waiting: ', x)
#     # await asyncio.sleep(x)
#     await hello_sleep(x)
#     return 'Done after {}s'.format(x)
@asyncio.coroutine
def hello_sleep(s):
    time.sleep(s)

@asyncio.coroutine
def do_some_work(x):
    print('Waiting: ', x)
    yield from asyncio.sleep(x)
    # yield from hello_sleep(x)
    return 'Done after {}s'.format(x)

start = now()

coroutine1 = do_some_work(1)
coroutine2 = do_some_work(2)
coroutine3 = do_some_work(4)
print (coroutine1)
tasks = [
    asyncio.ensure_future(coroutine1),
    asyncio.ensure_future(coroutine2),
    asyncio.ensure_future(coroutine3)
]
print(tasks[0])

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

for task in tasks:
    print('Task ret: ', task.result())

print('TIME: ', now() - start)

# Waiting:  1
# Waiting:  2
# Waiting:  4
# Task ret:  Done after 1s
# Task ret:  Done after 2s
# Task ret:  Done after 4s
# TIME:  3.993000030517578

# Waiting:  1
# Waiting:  2
# Waiting:  4
# Task ret:  Done after 1s
# Task ret:  Done after 2s
# Task ret:  Done after 4s
# TIME:  7.000999927520752

