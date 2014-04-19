#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc

#TODO: Replace classes by meta-classes?

class Message(object):
    """ base class for all messages """
    __metaclass__ = abc.ABCMeta
    
    def __init__(self):
        pass

    @abc.abstractmethod
    def _initialize(object):
        """ builds the message """
        pass

class FundamentalMessage(Message):
    pass

class MarketMessage(Message):
    pass

class NewsMessage(Message):
    pass
