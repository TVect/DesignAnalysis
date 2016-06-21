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

class FIFODecorator(CacheMethodDecorator):
    def __init__(self, cache_method_component, limit_size=1024*1024*1024):
        super(FIFODecorator, self).__init__(cache_method_component, limit_size)
        
        self.cache_fifo_list = [] # 新添加的项按顺序加入，按顺序弹出


    def fetch_data(self, no):
        data_size = self.get_data_size(no)
        if not data_size:
            return

        self.total_count += 1   # 总的file请求次数加1
        self.byte_total_count += data_size  # 总的请求的字节数相应增加

        if no in self.cache_dict.keys():
            self.hit_count += 1     # 缓存命中次数加1
            self.byte_hit_count += data_size    # 命中的字节数相应增加
            return self.cache_dict[no]
        else:
            remote_data = self.cache_method_component.fetch_data(no)
            self.used_size += data_size

            if self.used_size <= self.limit_size:   # 有足够的空间可以用于存储
                self.cache_dict[no] = remote_data  # 更新缓存
                self.cache_fifo_list.append(no)
            else:   # 没有足够的空间用于缓存
                while self.used_size > self.limit_size:
                    pop_no = self.cache_fifo_list.pop(0)
                    del self.cache_dict[pop_no]
                    self.used_size -= self.get_data_size(pop_no)
                self.cache_dict[no] = remote_data
                self.cache_fifo_list.append(no)
            return remote_data

    def get_data_size(self, no):
        return module_size_dict.get(no, 0)
