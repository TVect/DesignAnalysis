#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.style.use('ggplot')

def visual_plot():
    with open("plugin_no.txt") as fr:
        count_list = []
        for line in fr.readlines():
            count_list.append(len(line.strip().split(",")))
    
    design_series = pd.Series(count_list)
    result = design_series.value_counts()
    
    (result.sort_index()).plot()
    plt.xlabel(u"设计中含有的模型数目")
    plt.ylabel(u"设计的个数")
    plt.locator_params('x', nbins=20)
    plt.title(u"设计中模型数目分布情况图 (设计总数: %s)" % design_series.size)
    plt.show()


def visual_boxplot():
    with open("plugin_no.txt") as fr:
        count_list = []
        for line in fr.readlines():
            count_list.append(len(line.strip().split(",")))
    
    design_series = pd.Series(count_list)
    plt.boxplot(design_series, notch=True, patch_artist=True, showmeans=True)
    plt.show()

if __name__ == "__main__":
    visual_boxplot()