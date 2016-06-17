#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

from numpy import random
import abc

class CacheMethod(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fetch_data(self):
        pass


class CacheMethodDecorator(CacheMethod):
    pass


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


class RandomDiscardDecorator(CacheMethodDecorator):
    def __init__(self, cache_method_component, limit=10):
        self.cache_method_component = cache_method_component
        self.cache_dict = {}
        self.limit = limit

        self.hit_count = 0
        self.total_count = 0

    def fetch_data(self, no):
        self.total_count += 1
        if no in self.cache_dict.keys():
            self.hit_count += 1
            print "******************cache hit: no =", no, 
            return self.cache_dict[no]
        else:
            data = self.cache_method_component.fetch_data(no)
            if len(self.cache_dict) >= self.limit:
                key = random.choice(self.cache_dict.keys())
                del(self.cache_dict[key])
            self.cache_dict[no] = data
            return data

    def show_info(self):
        print "total_count =", self.total_count,
        print "hit_count =", self.hit_count
        if self.cache_method_component:
            self.cache_method_component.show_info()


if __name__ == "__main__":
    cache_method = RandomDiscardDecorator(NullCache(), limit=500)
    cache_method = RandomDiscardDecorator(cache_method, limit=100)
    cache_method = RandomDiscardDecorator(cache_method, limit=20)
    for no in map(int, 100*random.randn(10000) + 10000):
        print cache_method.fetch_data(no)
#     print cache_method.cache_dict.keys()
    print cache_method.show_info()

