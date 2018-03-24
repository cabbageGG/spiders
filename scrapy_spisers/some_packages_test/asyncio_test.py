#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/15 15:32'

from time import strftime,time
import asyncio

async def doSomething(t):
    print(strftime("[%H:%M:%S]"),end=" ") #这里不会换行
    print('wait %d 秒' % t)
    await asyncio.sleep(t)
    print(strftime("[%H:%M:%S]"), end=" ")
    print('finish: %s' % t)
    return t

def start_with_asyncio(t_list):
    loop = asyncio.get_event_loop()
    tasks = [doSomething(i) for i in range(5)]
    loop.run_until_complete(asyncio.wait(tasks)) #这里会阻塞
    loop.close()
    print('finish')


if __name__ == "__main__":
    # s_time = time()
    # start_with_asyncio(range(4,-1,-1))
    # print("cost:%.2f秒" % (time()-s_time))
    from collections import deque
    d = deque([1,2,3])
    for i in d:
        print (i)

