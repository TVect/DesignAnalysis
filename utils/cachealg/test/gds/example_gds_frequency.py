#coding:utf8
'''
@author: chin
@date: 2016年6月14日
'''

from cachealg.gds_frequency import GreedyDualSizeFrequency

import os
import random
from sourcedata import de_duplication

def gen_real_request_no(size=10):
    design_path = "sourcedata/design/data"
    name_list = os.listdir(design_path)
    random.shuffle(name_list)
    for name in name_list[:size]:
        filename = os.path.join(design_path, name)
        plugins = de_duplication(filename)
        for plugin in plugins:
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
