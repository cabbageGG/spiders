#-*- coding: utf-8 -*-

__author__ = 'liyangjin'
__time__ = '2018/1/14 9:31'

from collections import namedtuple

# user = namedtuple("User",("name","age","height"))
# print(user,user.__doc__) #<class '__main__.User'> User(name, age, height)
# # u = user("yj",25) #TypeError: __new__() missing 1 required positional argument: 'height'
# # u = user("yj",25,170)
# u = user(*("yj",25),height=170)
# print (u.name)
# print (u._asdict()) #OrderedDict([('name', 'yj'), ('age', 25), ('height', 170)])
# u1 = u._replace(name="yyj",height=175)
# print (u.name,u._asdict()) #('yj', OrderedDict([('name', 'yj'), ('age', 25), ('height', 170)]))
# print (u1.name,u1._asdict()) #('yyj', OrderedDict([('name', 'yyj'), ('age', 25), ('height', 175)]))
""" 
1、namedtuple实质是创建一个类User，并指明类里包含哪些成员变量(name,age,height)。
2、namedtuple将创建的类起了个别名叫user。
   注：我们只能用user(name,age,height)来创建类的实例，而不能用大写的。
       因此，通常的做法是：User=namedtuple("User",("name","age","heigth"))保证两个的值是一样的。
3、初始化传参：可以是位置参数或者是关键字参数 u = user("yj",age=25,height=170)
4、可以使用_asdict()来获得一个OrderedDict
5、使用_replace(**kw)来更新值。 
   注：这里的更新操作，会返回一个新的实例！！！！

优势：替代常规的类的定义，节省代码和空间。
        
"""

from collections import defaultdict

# users = ['qq1','qq2','qq1','qq3','qq2']
# d = dict()
# for user in users:
#     d.setdefault(user,0)
#     d[user] += 1 #KeyError: 'qq1'
# print (d) #{'qq1': 2, 'qq3': 1, 'qq2': 2}

# d = defaultdict(int) #注：需要传递一个可调用对象，作为value的类型。 （函数也是一个可调用对象！！！）
# for user in users:
#     d[user] += 1 
# print (d) #defaultdict(<type 'int'>, {'qq1': 2, 'qq3': 1, 'qq2': 2})

# def gen_default():
#     return {"name":'',"age":0}

# d = defaultdict(gen_default)
# print(d['test']) #{'age': 0, 'name': ''}

'''
1、defaultdict初始化，需要传递一个可调用对象，作为value的类型。 （函数也是一个可调用对象！！！）
2、defaultdict会有默认值。如，str:'',int:0
'''

from collections import deque

l = [1,2,4,3,6,5]
d = deque(l)  #deque([1, 2, 4, 3, 6, 5])
d.append('end') #deque([1, 2, 4, 3, 6, 5, 'end'])
d.appendleft('head') #deque(['head', 1, 2, 4, 3, 6, 5, 'end'])
d.pop()   #deque(['head', 1, 2, 4, 3, 6, 5])
d.popleft() #deque([1, 2, 4, 3, 6, 5])
d.extend([11]) #deque([1, 2, 4, 3, 6, 5, 11])
d.extendleft([22]) #deque([22, 1, 2, 4, 3, 6, 5, 11])

'''
1、deque是一个双端队列。相对于list增加了，头部操作！
   比如：appendleft,popleft,extendleft
2、deque GIL是线程安全的，list不是线程安全的！！！！
'''

from collections import Counter

d = Counter('aaasdf')
print (d)  #Counter({'a': 3, 's': 1, 'd': 1, 'f': 1})
print(d.most_common(2))  #[('a', 3), ('s', 1)]
print(d.elements()) #<itertools.chain object at 0x02697130>
print(sorted(d.elements()))  #['a', 'a', 'a', 'd', 'f', 's']
del d['a'] #删除所有的a ！！！                 
print(d)   #Counter({'s': 1, 'd': 1, 'f': 1})
d.update(Counter("sdgfda"))  #扩容
print(d)   #Counter({'d': 3, 's': 2, 'f': 2, 'a': 1, 'g': 1})
d['g'] -= 2 #减少计数，计数可以小于等于0。
print (d)  #Counter({'d': 3, 's': 2, 'f': 2, 'a': 1, 'g': -1})
d.clear() #清空
print(d)  #Counter()

'''
1、Counter统计输入的可迭代对象的频次。并按照频次的高低排序后，输出字典。字典的key为迭代对象，value为出现的频次！！
2、常用操作有：
   most_common(n)，输出一个list，保存前n的频次的key值。
   sorted(d.elements()) 排序key值，返回一个list。注意：是可以有重复的值的！！！
   del d['a'] 删除所有的a元素
   d.update(c) 将计数器c的值，扩充至d中。
   d.clear() 清空计数器
'''

from collections import OrderedDict
# d = dict()
# d['c'] = 'c'
# d['a'] = 'a'
# d['b'] = 'b'
# print(d) #{'a': 'a', 'c': 'c', 'b': 'b'}
# d = OrderedDict()
# d['c'] = 'c'
# d['a'] = 'a'
# d['b'] = 'b'
# print(d) #OrderedDict([('c', 'c'), ('a', 'a'), ('b', 'b')])
# print(d.popitem()) #('b', 'b')
# print(d) #OrderedDict([('c', 'c'), ('a', 'a')])
# # print(d.move_to_end('a'))
'''
1、OrderedDict是有序的，按照加入的顺序排放，dict在Python2中是无序的，在python3中也是默认有序的。
2、OrderedDict有一个popitem()函数，直接抛出最后一个元素。
3、在python3中，OrderedDict还有一个常用函数move_to_end('key')将某个key移动至末尾
'''






