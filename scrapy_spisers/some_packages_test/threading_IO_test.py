#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/15 11:04'

from time import sleep,strftime,time
import threading

def doSomething(t):
    print(strftime("[%H:%M:%S]"),end=" ") #这里不会换行
    print('wait %d 秒' % t)
    sleep(t)
    print(strftime("[%H:%M:%S]"), end=" ")
    print('finish: %s' % t)
    return t

if __name__ == "__main__":
    threads = []
    for i in range(4,-1,-1):
        t = threading.Thread(target=doSomething,args=(i,))
        threads.append(t)
    s_time = time()
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print("cost:%.2f秒" % (time()-s_time))


