#coding:utf8
'''
@author: chin
@date: 2016年6月2日
'''

from utils.cachealg.main.basic.base import CacheMethod, CachedData

# import random

class FirstInFirstOut(CacheMethod):
    
    def __init__(self, limit_size):
        super(FirstInFirstOut, self).__init__(limit_size)
        self.cache_list = []    # 给CachedData排序，最近访问的数据会放在cache_list的尾部，从头部删除数据
    
    
    def fetch_data(self, no):
        self.total_times += 1
        if no in self.cache_list:
            self.cache_hit_times += 1
#             idx = self.cache_list.index(no)
#             self.cache_list.pop(idx)
#             self.cache_list.append(no)    
            return self.cache_map[no].data
        
        remote_data = self.fetch_remote_data(no)
        if len(self.cache_map) >= self.limit_size:  #FIFO 删除的时候从cache_list的头开始删，因为头部是最先进来的
            del_no = self.cache_list.pop(0)
            del(self.cache_map[del_no])
#             random_no = self.cache_list.pop(random.randint(0, len(self.cache_list)-1))
#             del(self.cache_map[random_no])
            
        self.cache_map[no] = CachedData(remote_data)
        self.cache_list.append(no)
        return remote_data