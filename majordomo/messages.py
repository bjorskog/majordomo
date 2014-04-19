#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Messages will be separated on the prefix, then 
on the data type, e.g.:
data.fundamental, data.market, data.news, cmd.trade, cmd.heartbeat, 
cmd.price, cmd.depth, cmd.status 

Look up the Nordnet API for examples of feeds.
"""

#TODO: Make passing of class initialisor easier
#TODO: Replace classes by meta-classes?
#TODO: Move all classes to its own module for simplicity?

import json

class Message(object):
    """ base class for all messages """
    _messagetype = None
    _payload = None
    
    def __init__(self, messagetype, payload):
        self._messagetype = messagetype
        self._payload = payload
        #build the message
        self._initialize()

    def _initialize(self):
        """ builds the message """
        self._message = [self._messagetype, json.dumps(self._payload)]

    @property
    def messagetype(self):
        return self._messagetype

    @property
    def payload(self):
        return self._payload

    @property
    def message(self):
        return self._message
