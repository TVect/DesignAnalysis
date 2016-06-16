#coding:utf8
'''
@author: chin
@date: 2016年6月13日
'''

# import heapq
# import Queue
# import math
import pickle
import os

MODULE_SIZE_FILE = "module_size.list"
module_size_dict = dict(pickle.load(open(os.path.join(os.path.dirname(__file__), MODULE_SIZE_FILE))))

class GreedyDualSizeFrequency(object):
    def __init__(self, limit_size=1024*1024*1024):
        self.used_size = 0
        self.limit_size = limit_size
        
        self.hit_count = 0.0
        self.byte_hit_count = 0.0
        self.total_count = 0.0
        self.byte_total_count = 0.0

        self.cache_dict = {}
        self.cache_priority_queue = {}      #TODO 实现方式希望有一个类似的zset

        self.clock = 0      # 控制衰老

    def fetch_data(self, no):
        data_size = self.get_data_size(no)
        if not data_size:
            return None
        self.total_count += 1   # 总的file请求次数加1
        self.byte_total_count += data_size  # 总的请求的字节数相应增加

        if no in self.cache_dict.keys():
            self.hit_count += 1     # 缓存命中次数加1
            self.byte_hit_count += data_size    # 命中的字节数相应增加

            self.cache_dict[no].frequent += 1
            self.cache_priority_queue[no] = self.calc_priority(self.cache_dict[no].frequent,    # 更新优先级队列
                                                                data_size)
            return self.cache_dict[no].data
        else:
            remote_data = self.fetch_remote_data(no)
            remote_data_priority = self.calc_priority(1, data_size)
            self.cache_priority_queue[no] = remote_data_priority    # 更新优先队列
            self.used_size += data_size

            if self.used_size <= self.limit_size:   # 有足够的空间可以用于存储
                self.cache_dict[no] = self.CachedData(remote_data)  # 更新缓存
            else:   # 没有足够的空间用于缓存
                evict_files = self.find_files_to_evict()
                if no in evict_files:   # remote_data不应该被缓存
                    self.used_size = self.used_size - self.get_data_size(no)
                    del(self.cache_priority_queue[no])
                else:   # remote_data应该被缓存
                    self.clock = self.cache_priority_queue[evict_files[-1]] # 将 clock 更新为被替换出去的 file 中 priority 最大者
                    print "缓存替换: clock=", self.clock
                    for evict_file in evict_files:
                        del(self.cache_priority_queue[evict_file])
                        del(self.cache_dict[evict_file])
                        self.used_size -= self.get_data_size(evict_file)
                    self.cache_dict[no] = self.CachedData(remote_data)


    def find_files_to_evict(self):
        '''
        找到优先级最低的 k个文件，使得这k个缓存文件被剔除后，可以使得self.used_size < self.limit_size
        '''
        evict_files = []
        used_estimate = self.used_size
        sorted_priority_list = sorted(self.cache_priority_queue.iteritems(), key=lambda item: item[1])
        for file_no, _ in sorted_priority_list:
            evict_files.append(file_no)
            used_estimate -= self.get_data_size(file_no)
            if used_estimate < self.limit_size:
                break
#             if self.used_size - file_priority < self.limit_size:
#                 break
        return evict_files


    def calc_priority(self, freq, size):
#         cost = 1
        cost = (2 + size/536)
        return self.clock + freq * cost/float(size)
#         return self.clock + freq * cost / math.log(size)
#         return self.clock + freq * cost
#         return self.clock + freq * 1 / math.log(size)
#         return self.clock + freq * 1 / float(size)


    def get_data_size(self, no):
        return module_size_dict.get(no, 0)


    def fetch_remote_data(self, no):
        return "I am the remote file..."


    def hit_precent(self):
        return float(self.hit_count) / self.total_count


    def byte_hit_precent(self):
        return float(self.byte_hit_count) / self.byte_total_count


    class CachedData(object):
        def __init__(self, data, frequent=1):
            self.data = data
            self._frequent = frequent

        @property
        def frequent(self):
            return self._frequent

        @frequent.setter
        def frequent(self, freq):
            self._frequent = freq
