#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import sys
sys.path.append("..")

from base import CacheMethod

class NullCache(CacheMethod):
    def __init__(self):
        self.request_dict = {}

    def fetch_data(self, no):
        self.request_dict[no] = self.request_dict.get(no, 0) + 1
        return self.fetch_remote_data(no)

    def fetch_remote_data(self, no):
        remote_data = "fetch remote data: no = %s" % no
        return remote_data

    def show_info(self):
        request_count = sum([value for _, value in self.request_dict.iteritems()])
        print "request count =", request_count, "distinct request count =", len(self.request_dict)
#         for key, value in sorted(self.request_dict.items(), key = lambda item: item[1], reverse = True):
#             print key, value
