#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import abc
import json

class CacheMethod(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fetch_data(self):
        pass


class CacheMethodDecorator(CacheMethod):
    
    def __init__(self, cache_method_component, limit_size=1024*1024*1024):
        self.cache_method_component = cache_method_component
        self.limit_size = limit_size
        
        self.used_size = 0
        self.hit_count = 0.0
        self.byte_hit_count = 0.0
        self.total_count = 0.0
        self.byte_total_count = 0.0

        self.cache_dict = {}
    
    def save_result(self, filename):
        ret_dict = {"method": str(self.__class__),
                    "limit_size": self.limit_size,
                    "used_size": self.used_size,
                    "total_count": self.total_count,
                    "hit_count": self.hit_count,
                    "hit_precent": float(self.hit_count)/self.total_count,
                    "byte_total_count": self.byte_total_count,
                    "byte_hit_count": self.byte_hit_count,
                    "byte_hit_precent": float(self.byte_hit_count)/self.byte_total_count}
        ret_str = json.dumps(ret_dict)+"\n"
        print ret_str
        with open(filename, "a") as fw:
            fw.write(ret_str)

    def show_info(self):
        print "--------", self.__class__, "--------"
        print "cache_size =", len(self.cache_dict), "byte_cache_size =", self.used_size 
        print "total_count =", self.total_count, "hit_count =", self.hit_count,
        print "hit_precent =", float(self.hit_count)/self.total_count
        print "byte_total_count =", self.byte_total_count, "byte_hit_count =", self.byte_hit_count,
        print "byte_hit_precent =", float(self.byte_hit_count)/self.byte_total_count
        if self.cache_method_component:
            self.cache_method_component.show_info()