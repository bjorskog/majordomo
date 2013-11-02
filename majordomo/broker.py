#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing

import zmq
from zmq.utils import jsonapi
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream


class Broker(multiprocessing.Process):
    """ pub-sub broker to provide conectivity 
    for the publisher of data and the writer/other listeners """

    _insocket = None
    _outsocket = None
    _loop = None
    _instream = None
    _outstream = None

    def __init__(self, inaddress, outadress):
        """ constructor """
        super(Broker, self).__init__()
        self._in_address = inaddress
        self._out_address = outadress

    def setup(self):
        """ sets up all the sockets, connections and streams """
        context = zmq.Context()
        self._insocket = context.socket(zmq.SUB)
        self._outsocket = context.socket(zmq.PUB)
        
        self._insocket.bind(self._in_address)
        self._insocket.setsockopt(zmq.SUBSCRIBE, '')
        self._outsocket.bind(self._out_address)
        
        self._loop = IOLoop.instance()

    def run(self):
        """ starts the eventloop """
        self.setup()
        self._instream = ZMQStream(self._insocket)
        #self._outstream = ZMQStream(self._outsocket)
        
        self._instream.on_recv(self._messagehandler)

        try:
            self._loop.start()
        except KeyboardInterrupt:
            pass

    def _messagehandler(self, msg):
        """ how to react on incomming messages """
        self._outsocket.send(msg)

def main():
    pub_address = 'tcp://127.0.0.1:5000'
    sub_address = 'tcp://127.0.0.1:6000'

    broker = Broker(pub_address, sub_address)
    broker.start()

if __name__ == "__main__":
    main()
