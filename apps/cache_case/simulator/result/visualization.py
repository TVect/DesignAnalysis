#coding:utf8
'''
@author: chin
@date: 2016年6月21日
'''

import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import json

matplotlib.style.use('ggplot')

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