#coding:utf8
'''
@author: chin
@date: 2016年6月16日
'''

'''
gds下的缓存替换算法，即为GreedyDualSize系列算法，是GreedyDual的改进。
GreedyDual试图使得缓存的每一项价值尽量大，而GreedyDualSize试图使得缓存的每一个字节价值尽量大。
GreedyDual适合用来处理缓存条目总数有上限限制的情况，或者是缓存字节总数有上限，但每一缓存项大小相同的情况。
GreedyDualSize适合用来处理缓存字节总数有上限限制的情况。

'''

from gds_frequency import GreedyDualSizeFrequency