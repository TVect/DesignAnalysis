#coding:utf8
'''
@author: chin
@date: 2016年6月2日
'''

from utils.cachealg.main.basic.base import CacheMethod, CachedData


class LeastRecentlyUsed(CacheMethod):
    
    def __init__(self, limit_size):
        super(LeastRecentlyUsed, self).__init__(limit_size)
        self.cache_list = []    # 给CachedData排序，最近访问的数据会放在cache_list的尾部，从头部删除数据
        self.cache_map = {}
    
    def fetch_data(self, no):
        self.total_times += 1
        if no in self.cache_list:
            self.cache_hit_times += 1
            idx = self.cache_list.index(no)
            self.cache_list.pop(idx)
            self.cache_list.append(no)  #刚刚访问到的数据放到cache_list的末尾
            return self.cache_map[no].data
        
        remote_data = self.fetch_remote_data(no)
        if len(self.cache_map) >= self.limit_size:  #删除的时候从cache_list的头开始删，因为头部是LeastRecentlyUsed的
            del_no = self.cache_list.pop(0)
            del(self.cache_map[del_no])
        
        self.cache_map[no] = CachedData(remote_data)
        self.cache_list.append(no)
        return remote_data
        
    
#     def show_cache_info(self):
#         super(LeastFrequentlyUsed, self).show_cache_info()
#         print "------------------------------------------------------------------"
#         for key, item in self.cache_map.items():
#             print key, item.visited_times