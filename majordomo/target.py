#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

class Target(object):
    """ representation of a final destination """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def exists(self):
        pass

class FileTarget(Target):
    """ interface for writing to file """
    pass

class MongoTarget(Target):
    """ interface for writing to MongoDB """
    pass

class ZmqTarget(Target):
    """ interface for writing to the bus """
    pass
