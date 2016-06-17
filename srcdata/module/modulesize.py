#coding:utf8
'''
@author: chin
@date: 2016年6月8日
'''

import lxml.etree
import os
import pickle
from optparse import OptionParser

def walk_module_dir(module_dir, save_file="module_size.list"):
    module_list = []
    for module_no in os.listdir(module_dir):
        module_path = os.path.join(module_dir, module_no)
        
        total_size = 0
        try:
            total_size += os.path.getsize(os.path.join(module_path, "item.obj"))
        except Exception as e:
            pass
        
        try:
            total_size += os.path.getsize(os.path.join(module_path, "item.ocs"))
            doc = lxml.etree.parse(open(os.path.join(module_path, "item.ocs")))
            for node in doc.xpath("//pin/node/attr[@name=$name]", name="filename"):
                obj_name = node.text.replace("\\", "/")
                try:
                    total_size += os.path.getsize(os.path.join(module_path,obj_name))
                except Exception as e:
                    print e
        except Exception as e:
            print e
            
        print "module_no:", module_no, "total_size:", total_size
        module_list.append((module_no, total_size))

    pickle.dump(module_list, open(save_file, "w"))


if __name__ == "__main__":
    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)  
    parser.add_option("-d", "--dirname", dest="dirname", help="directory of the modules")
    parser.add_option("-f", "--filename", dest="save_file", help="file for save")
    (options, args) = parser.parse_args()  
#     if len(args) != 1:
#         parser.error("incorrect number of arguments, args=%s" % args)  
    if options.dirname:
        dirname = options.dirname
        save_file = "./module_size.list"
        if options.save_file:
            save_file = options.save_file
        walk_module_dir(dirname, save_file)
