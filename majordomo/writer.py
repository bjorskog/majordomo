#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import pymongo
import datetime

import json
import zmq
from zmq.utils import jsonapi
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream

#TODO: should work
try:
    from majordomo.utils import to_json
except:
    to_json = lambda z: jsonapi.loads(z)

class MongoWriter(multiprocessing.Process):
    """ 
    Process that subscribes to the message bus and writes all relevant 
    feeds to MongoDB. """

    _socket = None
    _loop = None
    _stream = None

    def __init__(self, db_name, collection_name, socket_addr='tcp://127.0.0.1:6000'):
        """ binds the subscriber socket, connects to the DB and 
        sets up the collection """
        super(MongoWriter, self).__init__()
        self._db_name = db_name
        self._collection_name = collection_name
        self._socket_addr = socket_addr
        self._connect()
        
    def _connect(self):
        """ sets up the connection with MongoDB """
        self._conn = pymongo.Connection()
        self._db = self._conn[self._db_name]
        self._collection = self._db[self._collection_name]
    
    def add_document(self, doc):
        """ adds a document to the collection """
        try:
            self._collection.insert(doc)
        except Exception, e:
            return 'Caught error: %s' % e
    
    def _setup(self):
        """ makes the socket and loop """
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect(self._socket_addr)
        self._socket.setsockopt(zmq.SUBSCRIBE, '')
        self._loop = IOLoop.instance()

    def run(self):
        """ starts the loop and starts writing """
        self._setup()
        self._stream = ZMQStream(self._socket)
        self._stream.on_recv(self._messagehandler)
        try:
            self._loop.start()
        except KeyboardInterrupt:
            pass

    def _messagehandler(self, msg):
        """ code for handling a message """
        msg = self._doc_to_json(msg[0])
        sender, feed_type, payload = msg[:]
        payload = json.loads(payload)
        print "Got %s from %s: %s" % (feed_type, sender, payload)
        self.add_document(payload)
        
    def _doc_to_json(self, doc):
        return json.loads(to_json(doc))

def main():
    """ entry point """
    db_name = 'writer'
    collection_name = 'fundamental'
    writer = MongoWriter(db_name, collection_name)
    writer.start()

if __name__ == "__main__":
    main()
