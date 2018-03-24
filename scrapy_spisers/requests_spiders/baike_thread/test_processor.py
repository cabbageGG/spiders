#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2017/12/31 9:50'

from multiprocessing import Process,Manager,Pipe,Queue
from multiprocessing import Array,Value

# 基本流程是：需要两个队列，一个队列是待爬取的url，由服务进程产生，由各个子进程来消费取走；
#             另一个队列是新产生的url，由子进程产生，然后由服务进程来消费取走，同时服务进程辨别是否需要加入到第一个队列中。

# conn1,conn2 = Pipe(True)
# 如果是全双工的(构造函数参数为True)，则双端口都可接收发送，否则前面的端口用于接收，后面的端口用于发送。
# conn1 服务进程产生,子进程消费；conn2 子进程产生，服务进程消费

# q1 = Queue()
# q2 = Queue()
# q1 服务进程产生,子进程消费；q2 子进程产生，服务进程消费

#服务进程函数
def pro1(q1,q2):
    print("服务进程开始")
    q1.put('start')
    while True:
        a = q2.get()
        print("服务进程接收：%s" % a)
        if a == 'finish':
            break
        else:
            b = "服务进程处理-"+ a
            q1.put(b)
    print("服务进程结束")

#子进程函数
def pro2(q1,q2):
    print("子进程开始")
    while True:
        a = q1.get()
        print("子进程接收：%s" % a)
        if a == "start":
            for i in range(5):
                q2.put(str(i))
        else:
            break
    print("子进程结束")

if __name__ == "__main__":
    q1 = Queue()
    q2 = Queue()
    p1 = Process(target=pro1,args=(q1,q2))
    p2 = Process(target=pro2,args=(q1,q2))
    p1.start()
    p2.start()
    p1.join()
    p2.join()



