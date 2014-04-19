#!/usr/bin/env python 
# -*- coding: utf-8 -*-

import unittest
import requests
import pprint

from majordomo.task import Task
from majordomo.target import Target
from majordomo.messages import NewsMessage

API_URI = 'http://umm.nordpoolspot.com/api/umm/message/'
NUM = 11248

class InputUmm(Task):
    """ gets something from web """

    def __init__(self):
        super(InputUmm, self).__init__()

    def output(self):
        """ output of task """
        uri = API_URI + str(NUM) + '/'
        try:
            data = requests.get(uri).json()
            pprint.pprint(data)
        except Exception as ex:
            print ex
        return data
    
    def _run(self):
        """ retrieves the message """
        return self.output()

class TransformUmm(Task):
    """ doing something with the data """
    def requires(self):
        """ fetches the data """
        return [InputUmm()]

    def output(self):
        """ stores the data """
        pass

    def _run(self):
        """ does some processing """
        fields = ['id']
        res = {}
        for item in self.requires():
            data = item.output()
            for field in fields:
                res[field] = data[field]
        print ''.join('\n')
        for item, key in res.iteritems():
            print "%s: %s" % (item, key)
        
class TestTask(unittest.TestCase):
    """ testing a simple task """
    def setUp(self):
        pass

    def test_transform(self):
        """ doing a simple transform """
        print '\n'
        task = TransformUmm()
        task.run()

    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
