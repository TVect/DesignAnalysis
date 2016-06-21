#coding:utf8
'''
@author: chin
@date: 2016年6月16日
'''


from utils.cachealg.main.gds import GreedyDualSizeFrequency

import random

def gen_real_request_no(size=10):
    plugin_file = "../../srcdata/design/plugin_no.txt"
    design_list = []
    with open(plugin_file) as fr:
        for line in fr.readlines():
            design_list.append(line.strip().split(','))
#     random.shuffle(design_list)
    for design in design_list[:size]:
        for plugin in design:
            yield plugin

def test_gds():
    gds_method_list = [GreedyDualSizeFrequency(limit_size=1024*1024*1024*1024)]


    request_times = 5000
    request_no_set = set()
    for request_no in gen_real_request_no(size=request_times):
        for gds_method in gds_method_list:
            gds_method.fetch_data(request_no)
        request_no_set.add(request_no)


    for idx, gds_method in enumerate(gds_method_list):
        print "distinct requent count = ", len(request_no_set)
        print "cache_size =", len(gds_method_list[0].cache_dict), 
        print "byte_cache_size =", gds_method_list[0].used_size
#         print "hit_count =", gds_method.hit_count, "total_count =", gds_method.total_count, 
#         print "hit_precent =", gds_method.hit_precent()
#         print "byte_hit_count =", gds_method.byte_hit_count, "byte_total_count =", gds_method.byte_total_count, 
#         print "byte_hit_precent =", gds_method.byte_hit_precent()
        
        print "total_count =", gds_method.total_count, "hit_count =", gds_method.hit_count,
        print "hit_precent =", gds_method.hit_precent()
        print "byte_total_count =", gds_method.byte_total_count, "byte_hit_count =", gds_method.byte_hit_count,
        print "byte_hit_precent =", gds_method.byte_hit_precent()
        
        print "---------------------------------------------\n"


if __name__ == "__main__":
    import timeit
    t1 = timeit.Timer('test_gds()',
                      setup="from __main__ import test_gds")
    #only excute once
    print(t1.timeit(1))