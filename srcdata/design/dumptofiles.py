#coding:utf8
'''
@author: chin
@date: 2016年6月3日
'''

import config
import os

json_files = [os.path.join(config.PLUGIN_DIR, name) for name in os.listdir(config.PLUGIN_DIR)]

with open("plugin_no.txt", "wt") as fw:
    for single in json_files:
        design_id, create_date = single.split(os.sep)[-1].split("_")
        create_date = create_date.split(".")[0]
        plugin_nos = config.de_duplication(single)
        if plugin_nos:
            fw.write(",".join(plugin_nos)+"\n")
        print "----------finish: ", design_id