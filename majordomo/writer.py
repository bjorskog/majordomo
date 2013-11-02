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

#TODO: Add config for database, collection and socket
#TODO: Messagehandler

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
        
    def _connect(self):
        self._conn = pymongo.Connection()
        self._db = self._conn[self._db_name]
        self._collection = self._db[self._collection_name]
    
    def add_document(self, doc):
        """ adds a document to the collection """
        self._connect()
        try:
            self._collection.insert(doc)
        except Exception, e:
            return 'Caught error: %s' % e
    
    def setup(self):
        """ makes the socket and loop """
        context = zmq.Context()
        self._socket = context.socket(zmq.SUB)
        self._socket.connect(self._socket_addr)
        self._socket.setsockopt(zmq.SUBSCRIBE, '')
        self._loop = IOLoop.instance()

    def run(self):
        """ starts the loop and starts writing """
        self.setup()
        self._stream = ZMQStream(self._socket)
        self._stream.on_recv(self._messagehandler)
        try:
            self._loop.start()
        except KeyboardInterrupt:
            pass

    def _messagehandler(self, msg):
        """ code for handling a message """
        msg = json.loads(self._doc_to_json(msg[0]))
        sender, feed_type, payload = msg[:]
        payload = json.loads(payload)
        print "Got %s from %s: %s" % (feed_type, sender, payload)
        self.add_document(payload)
        
    def _doc_to_json(self, doc):
        return jsonapi.loads(doc)

    def get_document_by_keys(self, keys):
        """ Attempts to return a single document from database table that matches
        each key/value in keys dictionary. """
        print 'attempting to retrieve document using keys: %s' % keys
        try:
            return self._table.find_one(keys)
        except Exception,e:
            return 'Error: %s' % e

def main():
    db_name = 'writer'
    collection_name = 'fundamental'
    writer = MongoWriter(db_name, collection_name)
    writer.start()

if __name__ == "__main__":
    main()
