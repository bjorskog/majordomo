#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import multiprocessing

#TODO: check command-line argument or in config how many workers to use

#if sys.argv or something similar
NUM_WORKERS = multiprocessing.cpu_count()

class MajorDomo(object):
    """ The controller """
    
    _worker_pool = []

class Worker(object):
    """ instance taking care of all work """
    pass
