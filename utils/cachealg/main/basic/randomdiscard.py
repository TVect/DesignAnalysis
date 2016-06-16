#coding:utf8
'''
@author: chin
@date: 2016年6月1日
'''

from utils.cachealg.main.basic.base import CacheMethod, CachedData
import random

class RandomDiscard(CacheMethod):
    def fetch_data(self, no):
        self.total_times += 1
#         self.frac += 0.1    # 每一轮frac都会做一点增加，保证最近访问的元素权重会大一些，保证尽量drop掉最长时间没有访问的数据
        
        if no in self.cache_map.keys():
            self.cache_hit_times += 1
            cached_data = self.cache_map[no]
            cached_data.visited_times += 1
            return cached_data.data
        
        remote_data = self.fetch_remote_data(no)
        if len(self.cache_map) >= self.limit_size:
            random_no = random.choice(self.cache_map.keys())
            del(self.cache_map[random_no])
        self.cache_map[no] = CachedData(remote_data)
        return remote_data