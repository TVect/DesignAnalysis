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
    random.shuffle(design_list)
    for design in design_list[:size]:
        for plugin in design:
            yield plugin


if __name__ == "__main__":
    gds_method_list = [GreedyDualSizeFrequency()]


    request_times = 500
    request_no_set = set()
    for request_no in gen_real_request_no(size=request_times):
        for gds_method in gds_method_list:
            gds_method.fetch_data(request_no)
        request_no_set.add(request_no)


    for idx, gds_method in enumerate(gds_method_list):
        print "distinct requent count = ", len(request_no_set)
        print "len-cache_dict =", len(gds_method_list[0].cache_dict), 
        print "len-cache_priority_queue =", len(gds_method_list[0].cache_priority_queue)
        print "hit_count =", gds_method.hit_count, "total_count =", gds_method.total_count, 
        print "hit_precent =", gds_method.hit_precent()
        print "byte_hit_count =", gds_method.byte_hit_count, "byte_total_count =", gds_method.byte_total_count, 
        print "byte_hit_precent =", gds_method.byte_hit_precent()
        print "---------------------------------------------\n"
