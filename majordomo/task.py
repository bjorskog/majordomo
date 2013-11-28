#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

class Task(object):
    """ represents work to do """
    __metaclass__ = abc.ABCMeta
    
    _is_done = False
    
    def __init__(self):
        """ constructor """
        pass

    def run(self):
        self._is_done = True
        return self._run()

    def requires(self):
        """ dependencies """
        return []

    def output(self):
        """ target """
        return []

    @abc.abstractmethod
    def _run(self):
        pass

    @property
    def is_done(self):
        return self._is_done
