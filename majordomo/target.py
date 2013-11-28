#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

class Target(object):
    """ representation of a final destination """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, target):
        """ constructor """
        super(Target, self).__init__()
        self._target = target

class FileTarget(Target):
    """ interface for writing to file """
    pass

class MongoTarget(Target):
    """ interface for writing to MongoDB """
    pass
