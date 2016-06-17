#coding:utf8
'''
@author: chin
@date: 2016年6月17日
'''

import abc

class CacheMethod(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def fetch_data(self):
        pass


class CacheMethodDecorator(CacheMethod):
    pass