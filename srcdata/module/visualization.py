#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import numpy as np
import pickle

module_dict = dict(pickle.load(open("module_size.list")))

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.style.use('ggplot')

def visual_plot():
    module_series = pd.Series(module_dict)
    
    idx_list = []
    count_list = []
    
    for idx in range(100):
        idx_list.append(idx)
        count_list.append(module_series[(module_series <= idx*1024*1024) & (module_series > (idx-1)*1024*1024)].size)
    
    idx_list.append(100)
    count_list.append(module_series[(module_series > 99*1024*1024)].size)
    
    
    plt.plot(idx_list, count_list)
    plt.xlabel(u"module大小(1024*1024 bytes)")
    plt.ylabel(u"module个数")
    plt.locator_params("x", nbins=10)
    plt.title(u"module尺寸分布图 (modules个数: %s)" % module_series.size)
    plt.show()


def visual_boxplot():
    module_sizes = np.array(module_dict.values())
    module_sizes = module_sizes[module_sizes>0]
    ret_dict = plt.boxplot(module_sizes, notch=True, patch_artist=True, showmeans=True)
    print ret_dict
    plt.show()


if __name__ == "__main__":
    visual_boxplot()
