#coding:utf8
'''
@author: chin
@date: 2016年6月21日
'''

import pickle
import os
from base import CacheMethodDecorator

MODULE_SIZE_FILE = "module_size.list"
module_size_dict = dict(pickle.load(open(os.path.join(os.path.dirname(__file__), MODULE_SIZE_FILE))))

class LRUDecorator(CacheMethodDecorator):
    def __init__(self, cache_method_component, limit_size=1024*1024*1024):
        self.cache_method_component = cache_method_component
        self.limit_size = limit_size

        self.cache_dict = {}
        self.cache_recently_used_list = []

        self.used_size = 0.0
        self.hit_count = 0.0
        self.byte_hit_count = 0.0
        self.total_count = 0.0
        self.byte_total_count = 0.0


    def fetch_data(self, no):
        data_size = self.get_data_size(no)
        if not data_size:
            return

        self.total_count += 1   # 总的file请求次数加1
        self.byte_total_count += data_size  # 总的请求的字节数相应增加

        if no in self.cache_dict.keys():
            self.hit_count += 1     # 缓存命中次数加1
            self.byte_hit_count += data_size    # 命中的字节数相应增加

            self.cache_recently_used_list.pop(self.cache_recently_used_list.index(no))  # 更新cache最近访问队列
            self.cache_recently_used_list.append(no)

            return self.cache_dict[no]
        else:
            remote_data = self.cache_method_component.fetch_data(no)
            self.used_size += data_size

            if self.used_size <= self.limit_size:   # 有足够的空间可以用于存储
                self.cache_dict[no] = remote_data  # 更新缓存
                self.cache_recently_used_list.append(no)
            else:   # 没有足够的空间用于缓存
                while self.used_size > self.limit_size:
                    pop_no = self.cache_recently_used_list.pop(0)
                    del self.cache_dict[pop_no]
                    self.used_size -= self.get_data_size(pop_no)
                self.cache_dict[no] = remote_data
                self.cache_recently_used_list.append(no)
            return remote_data


    def get_data_size(self, no):
        return module_size_dict.get(no, 0)

    def show_info(self):
        print "LRUDecorator---------"
        print "cache_size =", len(self.cache_dict), "byte_cache_size =", self.used_size 
        print "total_count =", self.total_count, "hit_count =", self.hit_count,
        print "hit_precent =", float(self.hit_count)/self.total_count
        print "byte_total_count =", self.byte_total_count, "byte_hit_count =", self.byte_hit_count,
        print "byte_hit_precent =", float(self.byte_hit_count)/self.byte_total_count
        if self.cache_method_component:
            self.cache_method_component.show_info()