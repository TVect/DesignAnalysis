#coding:utf8
'''
@author: chin
@date: 2016年6月2日
'''

'''
比较各种不同的缓存命中算法下，缓存命中率的差别
'''

from cachealg import ImprovedGreedyDualSize, RandomDiscard, LeastFrequentlyUsed, LeastRecentlyUsed, FirstInFirstOut
import os
import random
from sourcedata import de_duplication
import numpy as np
import matplotlib.pyplot as plt
import json

design_path = "sourcedata/plugin/design"
name_list = os.listdir(design_path)
random.shuffle(name_list)

def gen_real_request_no(size=10):
    for name in name_list[:size]:
        filename = os.path.join(design_path, name)
        plugins = de_duplication(filename)
        for plugin in plugins:
            yield plugin


cache_method_classes = [ImprovedGreedyDualSize, RandomDiscard, LeastFrequentlyUsed, LeastRecentlyUsed, FirstInFirstOut]

# cache_size_list = list(np.linspace(50, 1000, 20))
cache_size_list = list(np.linspace(10, 150, num=15))
request_times = 1000

for cache_method_class in cache_method_classes:
    
    total_times_list = []
    cache_hit_times_list = []
    cache_hit_precent_list = []
    distinct_request_count_list = []
    
    for cache_size in cache_size_list:
        cache_method = cache_method_class(cache_size)
        
        request_no_set = set()
        
        for request_no in gen_real_request_no(size = request_times):
            cache_method.fetch_data(request_no)
            request_no_set.add(request_no)
        
        cache_method.show_cache_info()
        
        total_times, cache_hit_times, cache_hit_precent = cache_method.get_cache_info()
        total_times_list.append(total_times)
        cache_hit_times_list.append(cache_hit_times)
        cache_hit_precent_list.append(cache_hit_precent)
        distinct_request_count_list.append(len(request_no_set))
    
    with open(os.path.join("result/algcomp", cache_method_class.__name__), "w") as fw:
        data_dict = {"name": cache_method_class.__name__,
                     "distinct_request_count": distinct_request_count_list,
                     "total_times": total_times_list,
                     "cache_hit_times": cache_hit_times_list,
                     "cache_hit_precent": cache_hit_precent_list,
                     "cache_size": cache_size_list}
        json.dump(data_dict, fw)

         


# for cache_size in np.linspace(50, 1000, num=50):
#     cache_method_list = [ImprovedGreedyDualSize(cache_size), 
#                      RandomDiscard(cache_size), 
#                      LeastFrequentlyUsed(cache_size),
#                      LeastRecentlyUsed(cache_size),
#                      FirstInFirstOut(cache_size)]
#     for request_no in gen_real_request_no(size = request_times):
#         for gds_method in cache_method_list:
#             gds_method.fetch_data(request_no)
    