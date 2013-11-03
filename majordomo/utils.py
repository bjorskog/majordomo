#!/usr/bin/env python
# -*- coding: utf-8 -*-

from zmq.utils import jsonapi

to_json = lambda z: jsonapi.loads(z)
