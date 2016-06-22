#coding:utf8
'''
@author: chin
@date: 2016年6月21日
'''

import pickle
import os
from numpy import random
from base import CacheMethodDecorator

MODULE_SIZE_FILE = "module_size.list"
module_size_dict = dict(pickle.load(open(os.path.join(os.path.dirname(__file__), MODULE_SIZE_FILE))))

class RandomDiscardDecorator(CacheMethodDecorator):
    def __init__(self, cache_method_component, limit_size=1024*1024*1024):
        super(RandomDiscardDecorator, self).__init__(cache_method_component, limit_size)


    def fetch_data(self, no):
        data_size = self.get_data_size(no)
        if not data_size:
            return

        self.total_count += 1
        self.byte_total_count += data_size
        if no in self.cache_dict.keys():
            self.hit_count += 1
            self.byte_hit_count += data_size
#             print "******************cache hit: no =", no
            return self.cache_dict[no]
        else:
            data = self.cache_method_component.fetch_data(no)
            self.used_size += data_size
            while self.used_size > self.limit_size:
                key = random.choice(self.cache_dict.keys())
                del(self.cache_dict[key])
                self.used_size -= self.get_data_size(key)
            self.cache_dict[no] = data
#             if len(self.cache_dict) >= self.limit:
#                 key = random.choice(self.cache_dict.keys())
#                 del(self.cache_dict[key])
#             self.cache_dict[no] = data
#             return data


    def get_data_size(self, no):
        return module_size_dict.get(no, 0)
