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

class LFUDecorator(CacheMethodDecorator):
    
    method_describe = "LFUDecorator"
    
    def __init__(self, cache_method_component, limit_size=1024*1024*1024):
        super(LFUDecorator, self).__init__(cache_method_component, limit_size)

        self.cache_frequently_dict = {} # 记录每一项被访问的次数


    def fetch_data(self, no):
        data_size = self.get_data_size(no)
        if not data_size:
            return

        self.total_count += 1   # 总的file请求次数加1
        self.byte_total_count += data_size  # 总的请求的字节数相应增加

        if no in self.cache_dict.keys():
            self.hit_count += 1     # 缓存命中次数加1
            self.byte_hit_count += data_size    # 命中的字节数相应增加

            self.cache_frequently_dict[no] = self.cache_frequently_dict.get(no, 0) + 1  # 更新cache访问频率队列
            return self.cache_dict[no]
        else:
            remote_data = self.cache_method_component.fetch_data(no)
            self.used_size += data_size

            if self.used_size <= self.limit_size:   # 有足够的空间可以用于存储
                self.cache_dict[no] = remote_data  # 更新缓存
                self.cache_frequently_dict[no] = 1
            else:   # 没有足够的空间用于缓存
                sorted_dict = sorted(self.cache_frequently_dict.iteritems(), key = lambda item: item[1])
#                 while self.used_size > self.limit_size:
#                     pop_no = self.cache_recently_used_list.pop(0)
#                     del self.cache_dict[pop_no]
#                     self.used_size -= self.get_data_size(pop_no)
                for i_no, _ in sorted_dict:
                    del self.cache_dict[i_no]
                    del self.cache_frequently_dict[i_no]
                    self.used_size -= self.get_data_size(i_no)
                    if self.used_size <= self.limit_size:
                        break
                self.cache_dict[no] = remote_data
                self.cache_frequently_dict[no] = 1
            return remote_data


    def get_data_size(self, no):
        return module_size_dict.get(no, 0)
