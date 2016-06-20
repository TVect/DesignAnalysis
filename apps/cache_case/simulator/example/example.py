#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

from numpy import random
from linkedlist import SortedLinkedList, SortedLinkedNode
import abc



class CacheMethod(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fetch_data(self):
        pass


class CacheMethodDecorator(CacheMethod):
    pass


class NullCache(CacheMethod):
    def __init__(self):
        self.request_dict = {}

    def fetch_data(self, no):
        self.request_dict[no] = self.request_dict.get(no, 0) + 1
        return self.fetch_remote_data(no)

    def fetch_remote_data(self, no):
        remote_data = "I am the data: no = %s" % no
        return remote_data

    def show_info(self):
        request_count = sum([value for _, value in self.request_dict.iteritems()])
        print "NullCache---------"
        print "request count =", request_count, "distinct request count =", len(self.request_dict)
#         for key, value in sorted(self.request_dict.items(), key = lambda item: item[1], reverse = True):
#             print key, value


class RandomDiscardDecorator(CacheMethodDecorator):
    def __init__(self, cache_method_component, limit=10):
        self.cache_method_component = cache_method_component
        self.cache_dict = {}
        self.limit = limit

        self.hit_count = 0
        self.total_count = 0

    def fetch_data(self, no):
        self.total_count += 1
        if no in self.cache_dict.keys():
            self.hit_count += 1
            print "******************cache hit: no =", no, 
            return self.cache_dict[no]
        else:
            data = self.cache_method_component.fetch_data(no)
            if len(self.cache_dict) >= self.limit:
                key = random.choice(self.cache_dict.keys())
                del(self.cache_dict[key])
            self.cache_dict[no] = data
            return data

    def show_info(self):
        print "RandomDiscardDecorator---------"
        print "total_count =", self.total_count, "hit_count =", self.hit_count
        if self.cache_method_component:
            self.cache_method_component.show_info()



class GDSDecorator(CacheMethodDecorator):
    def __init__(self, cache_method_component, limit_size=100*1024):
        self.cache_method_component = cache_method_component
        self.cache_dict = {}
        self.cache_priority_sortedlist = SortedLinkedList()    # 优先级的队列
        
        self.clock = 0  # 控制衰老
        
        self.limit_size = limit_size
        self.used_size = 0

        self.hit_count = 0
        self.total_count = 0
        self.byte_hit_count = 0.0
        self.byte_total_count = 0.0


    def fetch_data(self, no):
#         print "no = ", no
        data_size = self.get_data_size(no)
        
        self.total_count += 1
        self.byte_total_count += data_size
        if no in self.cache_dict.keys():    # 所需数据在当前缓存中
            self.hit_count += 1
            self.byte_hit_count += data_size
            print "******************cache hit: no =", no,
            
            ret_node = self.cache_priority_sortedlist.pop_node(no)
            try:
                ret_node.freq += 1
            except Exception as e:
                print e
            new_priority = self.calc_priority(ret_node.freq, ret_node.size)
            ret_node.priority = new_priority
            self.cache_priority_sortedlist.add_node(ret_node)
            return self.cache_dict[no]
        else:   # 所需数据不再当前缓存中，需要从被装饰对象中获取
            remote_data = self.cache_method_component.fetch_data(no)
            remote_data_priority = self.calc_priority(1, data_size)

#             self.cache_priority_sortedlist.add_node(no, remote_data_priority)   
            # 添加no到优先队列
            remote_data_node = SortedLinkedNode(no, remote_data_priority)
            remote_data_node.freq = 1
            remote_data_node.size = data_size
            self.cache_priority_sortedlist.add_node(remote_data_node)

            self.used_size += data_size

            if self.used_size <= self.limit_size:   # 有足够的空间可以用于存储
                self.cache_dict[no] = remote_data  # 更新缓存
            else:   # 没有足够的空间用于缓存
                evict_files = self.find_files_to_evict()
                if evict_files:
                    evict_filenos = [node.no for node in evict_files]
                    if no in evict_filenos:   # remote_data不应该被缓存
                        self.used_size = self.used_size - data_size
                        self.cache_priority_sortedlist.pop_node(no)
                    else:   # remote_data应该被缓存
                        self.clock = evict_files[-1].priority   # 将 clock 更新为被替换出去的 file 中 priority 最大者
    #                     print "缓存替换: clock=", self.clock
                        for evict_file in evict_files:
                            self.cache_priority_sortedlist.pop_node(evict_file.no)
                            del(self.cache_dict[evict_file.no])
                            self.used_size -= evict_file.priority
                        self.cache_dict[no] = remote_data
            return remote_data


    def calc_priority(self, freq, size):
        cost = (2 + size/536)
        return self.clock + freq * cost/float(size)


    def find_files_to_evict(self):
        '''
        找到优先级最低的 k个文件，使得这k个缓存文件被剔除后，可以使得self.used_size < self.limit_size
        '''
        diff_size = self.used_size - self.limit_size
        if diff_size > 0:
            return self.cache_priority_sortedlist.find_least_node(diff_size)
        else:
            return None

    def get_data_size(self, no):
        return int(no)
    
    def show_info(self):
        print "GDSDecorator---------"
        print "total_count =", self.total_count, "hit_count =", self.hit_count
        print "byte_total_count =", self.byte_total_count, "byte_hit_count =", self.byte_hit_count
        if self.cache_method_component:
            self.cache_method_component.show_info()


def test_randomdiscard():
    cache_method = RandomDiscardDecorator(NullCache(), limit=100)
    cache_method = RandomDiscardDecorator(cache_method, limit=100)
    cache_method = RandomDiscardDecorator(cache_method, limit=20)
    for no in map(int, 100*random.randn(10000) + 10000):
        print cache_method.fetch_data(no)
#     print cache_method.cache_dict.keys()
    print cache_method.show_info()


def test_gds():
    print "start ----------"
    cache_method = GDSDecorator(NullCache(), limit_size=1024*1024)
    cache_method = RandomDiscardDecorator(cache_method)
    for no in map(int, 100*random.randn(1000) + 10000):
        print cache_method.fetch_data(no)
    print cache_method.show_info()
    

if __name__ == "__main__":
    test_gds()
    