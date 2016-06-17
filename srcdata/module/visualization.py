#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import pickle

module_dict = dict(pickle.load(open("module_size.list")))

module_series = pd.Series(module_dict)

idx_list = []
count_list = []

for idx in range(100):
    idx_list.append(idx)
    count_list.append(module_series[(module_series <= idx*1024*1024) & (module_series > (idx-1)*1024*1024)].size)

idx_list.append(100)
count_list.append(module_series[(module_series > 99*1024*1024)].size)

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.style.use('ggplot')

plt.plot(idx_list, count_list)
plt.xlabel(u"module大小(1024*1024 bytes)")
plt.ylabel(u"module个数")
plt.locator_params("x", nbins=10)
plt.title(u"module尺寸分布图 (modules个数: %s)" % module_series.size)
plt.show()
