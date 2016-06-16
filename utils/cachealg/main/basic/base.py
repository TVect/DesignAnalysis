#coding:utf8
'''
@author: chin
@date: 2016年6月1日
'''

import abc


class CachedData(object):
    MAX_TIMES = 20
    
    def __init__(self, data, eplased_time = 0):
        self.data = data
        self.eplased_time = eplased_time
        self._visited_times = 1
        self._priority = 0
    
    @property
    def visited_times(self):
        return self._visited_times
    
    @visited_times.setter
    def visited_times(self, times):
        if times < self.MAX_TIMES:
            self._visited_times = times
            
    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, new_priority):
        self._priority = new_priority





class CacheMethod(object):
    '''
             删除策略
     priority计算策略
    '''
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, limit_size, frac=0):
        self.limit_size = limit_size
        self.frac = frac
        self.cache_map = {}

        self.cache_hit_times = 0    # 缓存命中的次数
        self.total_times = 0        # 总的请求的次数

    
    @abc.abstractmethod
    def fetch_data(self, no):
        pass


    def fetch_remote_data(self, no):
        ret_data = "I am the data fetched from network, whose no is %s" % no
        return ret_data

    def show_cache_info(self):
        print "--------------type: ", type(self)
        print "total_times=", self.total_times,
        print " cache_hit_times=", self.cache_hit_times,
        print " cache_hit_probabity=", self.cache_hit_times / float(self.total_times),
        print " cached_data count=", len(self.cache_map)

        

    def get_cache_info(self):
        return self.total_times, self.cache_hit_times, float(self.cache_hit_times)/self.total_times