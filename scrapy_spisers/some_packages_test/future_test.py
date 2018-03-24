#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/15 11:44'

from concurrent.futures import ThreadPoolExecutor,as_completed
from time import sleep,strftime,time

MAX_WORKERS = 10

def doSomething(t):
    print(strftime("[%H:%M:%S]"),end=" ") #这里不会换行
    print('wait %d 秒' % t)
    sleep(t)
    print(strftime("[%H:%M:%S]"), end=" ")
    print('finish: %s' % t)
    return t

def start_with_future(t_list):
    workers = min(MAX_WORKERS,len(t_list))
    with ThreadPoolExecutor(workers) as executor:
        results = executor.map(doSomething,t_list)
        # to_do = []
        # for t in t_list:
        #     future = executor.submit(doSomething,t) #构建future任务
        #     to_do.append(future)
        #     print(strftime("[%H:%M:%S]"), end=" ")
        #     print('scheduled for %d: %s' % (t,future))
        # results = []
        # for future in as_completed(to_do):  #注：这里会阻塞，as_completed 返回future的结果，哪个future先完成，就打印他的结果。
        #     res = future.result()
        #     results.append(res)
        #     print(strftime("[%H:%M:%S]"), end=" ")
        #     print('%s -- result:%s' % (future,res))
    # print(list(results))
    return list(results)

if __name__ == "__main__":
    s_time = time()
    start_with_future(range(4,-1,-1))
    print("cost:%.2f秒" % (time()-s_time))