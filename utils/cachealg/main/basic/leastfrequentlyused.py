#coding:utf8
'''
@author: chin
@date: 2016年6月2日
'''

from utils.cachealg.main.basic.base import CacheMethod, CachedData
import sys

class LeastFrequentlyUsed(CacheMethod):
    
    def fetch_data(self, no):
        self.total_times += 1
        
        if no in self.cache_map.keys():
            self.cache_hit_times += 1
            cached_data = self.cache_map[no]
            cached_data.visited_times += 1
            return cached_data.data
        
        remote_data = self.fetch_remote_data(no)
        if len(self.cache_map) >= self.limit_size:  # 缓存不够，需要删除使用频率最低的缓存项
            min_key, _ = self.find_least_frequent_item()
            del(self.cache_map[min_key])
        self.cache_map[no] = CachedData(remote_data)
        return remote_data
    
    
    def find_least_frequent_item(self):
        min_key = None
        min_value = sys.float_info.max
        for key, item in self.cache_map.iteritems():
            if item.visited_times < min_value:
                min_key = key
                min_value = item.visited_times
#         print min_key, min_value
        return min_key, min_value
    
#     def show_cache_info(self):
#         super(LeastFrequentlyUsed, self).show_cache_info()
#         print "------------------------------------------------------------------"
#         for key, item in self.cache_map.items():
#             print key, item.visited_times