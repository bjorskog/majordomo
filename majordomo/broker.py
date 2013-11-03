#!/usr/bin/env python
# -*- coding: utf-8 -*-

import multiprocessing
import json

import zmq
from zmq.utils import jsonapi
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream

from majordomo.utils import to_json

class Broker(multiprocessing.Process):
    """ pub-sub broker to provide conectivity 
    for the publisher of data to the writer/other listeners """

    _insocket = None
    _outsocket = None
    _loop = None
    _instream = None
    _outstream = None

    def __init__(self, inaddress, outaddress):
        """ constructor """
        super(Broker, self).__init__()
        self._in_address = inaddress
        self._out_address = outaddress

    def setup(self):
        """ sets up all the sockets, connections and streams """
        context = zmq.Context()
        self._insocket = context.socket(zmq.ROUTER)
        self._outsocket = context.socket(zmq.DEALER)
        
        self._insocket.bind(self._in_address)
        self._outsocket.bind(self._out_address)
        
        self._loop = IOLoop.instance()

    def run(self):
        """ starts the eventloop """
        self.setup()
        self._instream = ZMQStream(self._insocket)
        self._instream.on_recv(self._messagehandler)

        try:
            self._loop.start()
        except KeyboardInterrupt:
            pass

    def _messagehandler(self, msg):
        """ how to react on incomming messages """
        sender, feed_type, payload = msg[:]
        payload = to_json(payload)
        print "Got %s from %s" % (feed_type, sender)
        out_msg = json.dumps(msg)
        self._outsocket.send_json(out_msg)

def main():
    in_address = 'tcp://127.0.0.1:5000'
    out_address = 'tcp://127.0.0.1:6000'

    broker = Broker(in_address, out_address)
    broker.start()

if __name__ == "__main__":
    main()
