#coding:utf8
'''
@author: chin
@date: 2016年6月1日
'''

'''
对于ImprovedGreedyDualSize_Modified算法
比较在不同参数值的情况下，算法节省的总数据量大小
'''

from cachealg import RandomDiscard, ImprovedGreedyDualSize_Modified
import os
import random
from sourcedata import de_duplication
import numpy as np
import matplotlib.pyplot as plt
import json
import pickle

def gen_real_request_no(size=10):
    design_path = "sourcedata/design/data"
    name_list = os.listdir(design_path)
    random.shuffle(name_list)
    for name in name_list[:size]:
        filename = os.path.join(design_path, name)
        plugins = de_duplication(filename)
        for plugin in plugins:
            yield plugin

module_size_dict = dict(pickle.load(open("./sourcedata/module/module_size.list")))

if __name__ == "__main__":
    cache_limit_size = 100
#     gds_method = ImprovedGreedyDualSize(cache_limit_size, frac=0, frac_incr=0.01)
#     random_method = RandomDiscard(cache_limit_size)

    gds_method_list = []
#     frac_list = np.linspace(0, 1, num=4)
#     frac_list = [0.01, 0.02]
    frac_list = [10]
    for frac_incr in frac_list:
        gds_method_list.append(ImprovedGreedyDualSize_Modified(cache_limit_size, frac=0, frac_incr=frac_incr, module_size_dict=module_size_dict))
    
    
    request_times = 100
    request_no_set = set()
    for request_no in gen_real_request_no(size=request_times):
#         print request_no
        for gds_method in gds_method_list:
            gds_method.fetch_data(request_no)
        request_no_set.add(request_no)

    
    for idx, gds_method in enumerate(gds_method_list):
        print "frac_incr =", gds_method.frac_incr
        print "cache_hit_times =", gds_method.cache_hit_times, "total_times =", gds_method.total_times, "hit_precent =", float(gds_method.cache_hit_times)/gds_method.total_times
        print "hit_data_size =", gds_method.hit_data_size, "total_data_size =", gds_method.total_data_size, "hit_data_precent =", float(gds_method.hit_data_size)/gds_method.total_data_size
        print "---------------------------------------------\n"



    # 结果展示
    precent_list = []
    cache_hit_list = []
    best_frac = 0
    best_precent = 0
    for idx, gds_method in enumerate(gds_method_list):
        total_times, cache_hit_times, cache_hit_precent = gds_method.get_cache_info()
        precent_list.append(cache_hit_precent)
        cache_hit_list.append(cache_hit_times)
        if best_precent < cache_hit_precent:
            best_precent = cache_hit_precent
            best_frac = frac_list[idx]
    
    print "best_frac=", best_frac, "    best_precent=", best_precent
    
    plt.plot(frac_list, precent_list, label="ImprovedGreedyDualSize")
    plt.title("distinct request = %d" % len(request_no_set))
    plt.xlabel("frac_incr")
    plt.ylabel("cache_hit precent")
    plt.legend(loc="best")
    plt.annotate("(%.3f, %.3f)" % (best_frac, best_precent), xy=(best_frac, best_precent))
    plt.show()

    # save to file
#     name = "cachesize-%s" % cache_limit_size
#     result_dict = {"name": name, "frac_incr": list(frac_list), "precent": precent_list, "cache_hit": cache_hit_list}
#     with open(os.path.join("result", "ImprovedGreedyDualSize", name), "w") as fw:
#         json.dump(result_dict, fw)
