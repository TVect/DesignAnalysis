#coding:utf8
'''
@author: chin
@date: 2016年6月21日
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json
import pandas as pd

matplotlib.style.use('ggplot')

def visual_diffalg():
    '''
    比较几种不同的cache alg之间在不同limit_size情况下的差异
    '''
    files = ["gds.result", "fifo.result", "lfu.result", "lru.result", "random.result"]
    
    for filename in files:
        limit_size_list = []
        hit_precent_list = []
        byte_hit_precent_list = []
        method = None
        with open(filename) as fr:
            for line in fr.readlines():
                tmp = json.loads(line.strip())
                limit_size_list.append(tmp["limit_size"])
                hit_precent_list.append(tmp["hit_precent"])
                byte_hit_precent_list.append(tmp["byte_hit_precent"])
                method = tmp["method"]
    #     plt.plot(limit_size_list, hit_precent_list, label=method.split(".")[-1].split("'")[0])
        plt.plot(limit_size_list, byte_hit_precent_list, label=method.split(".")[-1].split("'")[0])
    plt.ylabel("byte_hit_precent")
    plt.title("byte_hit_precent - limit_size")
    
    plt.xlabel("limit_size")
    
    plt.legend(loc="best")
    plt.show()


def visual_diffgds():
    '''
    比较gds中几种不同的priority计算方案的差异
    '''
    filename = "gds_compare.result"
    ret_list = []
    with open(filename) as fr:
        for line in fr.readlines():
            ret_list.append(json.loads(line.strip()))
    ret_df = pd.DataFrame.from_records(ret_list)
     
    axs = plt.subplot(111)
     
    for method in ret_df['method'].unique():
        query_str = "method == '%s'" % method
        ret_df.query(query_str).plot(x='limit_size', y="byte_hit_precent", label=method.split('+')[-1], ax = axs)
    plt.title("byte_hit_precent")
    plt.show()


if __name__ == "__main__":
    visual_diffgds()