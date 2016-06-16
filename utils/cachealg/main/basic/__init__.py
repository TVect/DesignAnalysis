#coding:utf8
'''
@author: chin
@date: 2016年6月16日
'''

'''
basic下的缓存替换算法，基本上针对的是每一个缓存项大小相同的情况
目前包括的缓存替换算法有：
    RandomDiscard: 随机替换
    FirstInFirstOut: 先进先出
    LeastRecentlyUsed(LRU): 最近最少使用置换算法,也就是首先淘汰最长时间未被使用的项
    LeastFrequentlyUsed(LFU): 最近最不常用置换算法,也就是淘汰一定时期内被访问次数最少的项
    GreedyDual: 
'''