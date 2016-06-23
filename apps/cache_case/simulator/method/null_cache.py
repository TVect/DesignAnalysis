#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import sys
sys.path.append("..")

from base import CacheMethod

import pickle
import os
MODULE_SIZE_FILE = "module_size.list"
module_size_dict = dict(pickle.load(open(os.path.join(os.path.dirname(__file__), MODULE_SIZE_FILE))))


class NullCache(CacheMethod):
    def __init__(self):
        self.request_dict = {}

    def fetch_data(self, no):
        self.request_dict[no] = self.request_dict.get(no, 0) + 1
        return self.fetch_remote_data(no)

    def fetch_remote_data(self, no):
        remote_data = "I am the data: no = %s" % no
        return remote_data

    def show_info(self):
        print "NullCache---------"
        request_count = sum([value for _, value in self.request_dict.iteritems()])
        print "request count =", request_count, "distinct request count =", len(self.request_dict)
        distinct_byte_count = sum([self.get_data_size(no) for no, _ in self.request_dict.iteritems()])
        total_byte_count = sum([self.get_data_size(no)*value for no, value in self.request_dict.iteritems()])
        print "distinct_byte_count =", distinct_byte_count, "total_byte_count =", total_byte_count
#         for key, value in sorted(self.request_dict.items(), key = lambda item: item[1], reverse = True):
#             print key, value


    def get_data_size(self, no):
        return module_size_dict.get(no, 0)