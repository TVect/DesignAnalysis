#coding:utf8
'''
@author: chin
@date: 2016年6月1日
'''

# import CacheMethod
from utils.cachealg.main.basic.base import CacheMethod, CachedData
# import math
import sys

class GreedyDual(CacheMethod):
    '''
    简化的模型，目前缺乏对elasped_time的考虑
    '''
    
    def __init__(self, limit_size, frac=0, frac_incr=0.01): # 目前验证的情况下frac_incr是比较好的一个参数值
        super(GreedyDual, self).__init__(limit_size, frac)
        self.frac_incr = frac_incr
    
    def fetch_data(self, no):
        self.total_times += 1
#         self.frac += 0.01    # 每一轮frac都会做一点增加，保证最近访问的元素权重会大一些，保证尽量drop掉最长时间没有访问的数据
        self.frac += self.frac_incr
        
        if no in self.cache_map.keys():
            self.cache_hit_times += 1
            cached_data = self.cache_map[no]
            cached_data.visited_times += 1
            cached_data.priority = self.calc_priority(len(cached_data.data), cached_data.visited_times)
            return cached_data.data
        
        remote_data = self.fetch_remote_data(no)
        data_size = len(remote_data)
        if len(self.cache_map) >= self.limit_size:  # 缓存已满，考虑要不要进行替换，替换哪一个
            min_key, min_value = self.get_lowest_data()
            if self.calc_priority(data_size, 1) > min_value:
                del(self.cache_map[min_key])
#                 self.frac = min_value
                self.cache_map[no] = CachedData(remote_data)
                self.cache_map[no].priority = self.calc_priority(data_size, 1)
            return remote_data
        else:   # 缓存未满，直接将新的数据进行缓存
            self.cache_map[no] = CachedData(remote_data)
            self.cache_map[no].priority = self.calc_priority(data_size, 1)
            return remote_data


    def calc_priority(self, data_size, visited_times):
        return self.frac + visited_times*1
#         return self.frac + (visited_times - 1)*2
    
#     def calc_priority(self, data_size, visited_times):
#         return self.frac + 0.5 + visited_times - 1


    def get_lowest_data(self):
        min_key = None
        min_value = sys.float_info.max
        for key, item in self.cache_map.iteritems():
            if item.priority < min_value:
                min_key = key
                min_value = item.priority
        return min_key, min_value
    
    
    def show_cache_info(self):
        print "--------------type: ", type(self), "-----frac=", self.frac, "-----frac_incr=", self.frac_incr
        print "total_times=", self.total_times,
        print " cache_hit_times=", self.cache_hit_times,
        print " cache_hit_probabity=", self.cache_hit_times / float(self.total_times),
        print " cached_data count=", len(self.cache_map)



    #TODO 交叉验证确定最佳的参数值   
