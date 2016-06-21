#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import math
import pickle
import os
from base import CacheMethodDecorator

MODULE_SIZE_FILE = "module_size.list"
module_size_dict = dict(pickle.load(open(os.path.join(os.path.dirname(__file__), MODULE_SIZE_FILE))))

class GDSDecorator(CacheMethodDecorator):
    def __init__(self, cache_method_component, limit_size=1024*1024*1024):
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
        data_size = self.get_data_size(no)
        if not data_size:
            return None
        self.total_count += 1
        self.byte_total_count += data_size
        if no in self.cache_dict.keys():    # 所需数据在当前缓存中
            self.hit_count += 1
            self.byte_hit_count += data_size
#             print "******************cache hit: no =", no,
            
            ret_node = self.cache_priority_sortedlist.pop_node(no)
            try:
                ret_node.freq += 1
            except Exception as e:
                print e
            new_priority = self.calc_priority(ret_node.freq, ret_node.size)
            ret_node.priority = new_priority
            self.cache_priority_sortedlist.add_node(ret_node)
#             print "缓存更新: no =", no, "priority =", new_priority
            return self.cache_dict[no]
        else:   # 所需数据不再当前缓存中，需要从被装饰对象中获取
            remote_data = self.cache_method_component.fetch_data(no)
            remote_data_priority = self.calc_priority(1, data_size)

            # 添加no到优先队列
            remote_data_node = SortedLinkedNode(no, remote_data_priority)
            remote_data_node.freq = 1
            remote_data_node.size = data_size
            self.cache_priority_sortedlist.add_node(remote_data_node)

            self.used_size += data_size

            if self.used_size <= self.limit_size:   # 有足够的空间可以用于存储
                self.cache_dict[no] = remote_data  # 更新缓存
#                 print "缓存添加: no =", no, "priority =", remote_data_priority, "size =", data_size
            else:   # 没有足够的空间用于缓存
                evict_files = self.find_files_to_evict()
                if evict_files:
                    evict_filenos = [node.no for node in evict_files]
                    if no in evict_filenos:   # remote_data不应该被缓存
                        self.used_size = self.used_size - data_size
                        self.cache_priority_sortedlist.pop_node(no)
                    else:   # remote_data应该被缓存
                        self.clock = evict_files[-1].priority   # 将 clock 更新为被替换出去的 file 中 priority 最大者
#                         print "缓存替换: clock =", self.clock, "no =", no, "priority =", remote_data_priority
                        for evict_file in evict_files:
                            self.cache_priority_sortedlist.pop_node(evict_file.no)
                            del(self.cache_dict[evict_file.no])
                            self.used_size -= evict_file.size
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
        if diff_size >= 0:
            return self.cache_priority_sortedlist.find_least_node(diff_size)
        else:
            return None

    def get_data_size(self, no):
        return module_size_dict.get(no, 0)
    
    def show_info(self):
        print "GDSDecorator---------"
        print "cache_size =", len(self.cache_dict), "byte_cache_size =", self.used_size 
        print "total_count =", self.total_count, "hit_count =", self.hit_count,
        print "hit_precent =", float(self.hit_count)/self.total_count
        print "byte_total_count =", self.byte_total_count, "byte_hit_count =", self.byte_hit_count,
        print "byte_hit_precent =", float(self.byte_hit_count)/self.byte_total_count
        if self.cache_method_component:
            self.cache_method_component.show_info()


class SortedLinkedList(object):
    def __init__(self):
        self.head = SortedLinkedNode("root", 0)
    
    def add_node(self, node):
        pointer = self.head
        while pointer.next:
            if pointer.next.priority >= node.priority:
                node.next = pointer.next
                pointer.next = node
                break
            pointer = pointer.next
        else:
            pointer.next = node
            node.next = None

    def pop_node(self, no):
        pointer = self.head
        while pointer.next:
            if pointer.next.no == no:
                ret_node = pointer.next
                pointer.next = pointer.next.next
                return ret_node
            pointer = pointer.next
        return None
    
    def get_node(self, no):
        pointer = self.head
        while pointer.next:
            if pointer.next.no == no:
                return pointer.next
            pointer = pointer.next
        return None

    def find_least_node(self, lower_size):
        '''
        寻找最小的no，priority使得其和大于priority
        '''
        pointer = self.head
        node_list = []
        priority_sum = 0.0
        while pointer.next:
            pointer = pointer.next
            node_list.append(pointer)
            priority_sum += pointer.size
            if priority_sum >= lower_size:
                return node_list    # 成功找到一系列的no，使得它们的priority之和刚好大于priority
        return None # 无法找到符合条件的no_list，也就是说所有priority之和也还比priority要小

        
class SortedLinkedNode(object):
    def __init__(self, no, priority):
        self.next = None
        self.no = no
        self.priority = priority


#########################################
# OrderedHashMap
#########################################

import bisect

class OrderedHashMap(object):
    def __init__(self):
        self.key2node = {}  # no与其数据的对应
        self.ordered_list = []  # 按priority排序之后的node
    
    def add_node(self, node):
        self.key2node[node.no] = node
#         bisect_left(self.ordered_list, node)
        bisect.insort_left(self.ordered_list, node)
        
    
    def pop_node(self):
        pass
    
    def get_node(self, no):
        return self.key2node[no]
    
    def del_node(self, no):
        node = self.key2node.get(no)
        if not node:
            return 0
        del self.orderlist[self.findpos(no)]
        del self.key2node[no]
        del node
        return 1
    
    def find_least_node(self, lower_size):
        '''
        寻找最小的no，priority使得其和大于priority
        '''
        pointer = self.head
        node_list = []
        priority_sum = 0.0
        while pointer.next:
            pointer = pointer.next
            node_list.append(pointer)
            priority_sum += pointer.size
            if priority_sum >= lower_size:
                return node_list    # 成功找到一系列的no，使得它们的priority之和刚好大于priority
        return None # 无法找到符合条件的no_list，也就是说所有priority之和也还比priority要小
        
        node_list = []
        size_sum = 0.0
        for node in self.ordered_list:
            node_list.append(node)
            size_sum += node.size
            if size_sum > lower_size:
                return node_list
        return None

    
    def _find_pos(self, no):
        node = self.key2node(no)
        pos = bisect.bisect_left(self.ordered_list, node)
        while True:
            if self.ordered_list[pos].no == no:
                break
            pos += 1
        return pos

class DataNode(object):
    def __init__(self, no, data, priority):
        self.no = no
        self.priority = priority
        self.data = data
        self.freq = 1

    def __lt__(self,other):
        return self.priority < getattr(other,'priority', 0)

    def __gt__(self,other):#没定义__gt__的话会导致bisect_right出问题,即使已经定义了__lt__
        return self.priority > getattr(other,'priority', 0)
