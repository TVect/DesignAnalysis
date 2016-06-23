#coding:utf8
'''
@author: chin
@date: 2016年6月20日
'''

from method import GDSDecorator, NullCache
from method.random_discard import RandomDiscardDecorator
from method.lru import LRUDecorator
from method.lfu import LFUDecorator
from method.fifo import FIFODecorator
from method.gds_frequency2 import GDS2Decorator
from method.gds_frequency2 import calc_priority_1, calc_priority_2, \
                    calc_priority_3, calc_priority_4, calc_priority_5, calc_priority_6
from numpy import random
import numpy as np

def gen_real_request_no(size=10):
    plugin_file = "plugin_no.txt"
    design_list = []
    with open(plugin_file) as fr:
        for line in fr.readlines():
            design_list.append(line.strip().split(','))
#     random.shuffle(design_list)
    for design in design_list[:size]:
        for plugin in design:
            yield plugin


def test_diff_algs():
    print "start ----------"
    request_times = -1

    size_list = np.linspace(1, 10, 10) * 1024 * 1024 * 1024
    for size in size_list:
        print "size =", size
#         cache_method = FIFODecorator(NullCache(), limit_size=size)
#         cache_method = LFUDecorator(NullCache(), limit_size=size)
#         cache_method = LRUDecorator(NullCache(), limit_size=size)
        cache_method = RandomDiscardDecorator(NullCache(), limit_size=size)
#         cache_method = GDS2Decorator(NullCache(), limit_size=size)
        for idx in range(2):
            print "idx =", idx 
            for no in gen_real_request_no(size=request_times):
                cache_method.fetch_data(no)
        print cache_method.show_info()
#         print cache_method.save_result("result/gds.result")


def test_gds_diffmethods():
    request_times = -1
    size_list = np.linspace(1, 10, 10) * 1024 * 1024 * 1024
    calc_priority_methods = [calc_priority_1, calc_priority_2,calc_priority_3, 
                             calc_priority_4, calc_priority_5, calc_priority_6]
    for size in size_list:
        for method in calc_priority_methods:
            cache_method = GDS2Decorator(NullCache(), limit_size=size, calc_priority_method = method)
            for no in gen_real_request_no(size=request_times):
                cache_method.fetch_data(no)
            cache_method.show_info()
            cache_method.save_result("result/gds_compare.result")


if __name__ == "__main__":
#     test_gds()
    import timeit
    t1 = timeit.Timer('test_diff_algs()', setup="from __main__ import test_diff_algs")
#     t1 = timeit.Timer('test_gds_diffmethods()', setup="from __main__ import test_gds_diffmethods")
    #only excute once
    print(t1.timeit(1))
