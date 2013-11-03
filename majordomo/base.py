#!/usr/bin/env python
# -*- coding: utf-8 -*-

import abc
import multiprocessing

import zmq
from zmq.eventloop.ioloop import IOLoop
from zmq.eventloop.zmqstream import ZMQStream

from majordomo.utils import to_json

#TODO: fix for general socket types
#TODO: fix setting up of subscriptions
#TODO: add workers running in thread-pool
#TODO: add workers on scheduling
#TODO: add controller for firing off workers

class BaseProcessWorker(multiprocessing.Process):
    """ Template for all workers pushing data to the broker. This
    class is for tasks needing a single process to run in """

    __metaclass__ = abc.ABCMeta

    _context = None
    _socket = None
    _stream = None
    _loop = None

    _address = None
    _host = None
    _port = None

    def __init__(self, address, sock_type=None, context=None, bind=False):
        """ constructor """
        super(BaseProcessWorker, self).__init__()
        self._address = address
        host, port = self._parse_address(address)
        self._host = host
        self._port = port
        if not sock_type:
            sock_type = zmq.DEALER
        self._sock_type = sock_type
        self._context = context
        self._bind = bind

    def _setup(self):
        """ setup the socket """
        context = self._context
        if not context:
            context = zmq.Context()
        self._socket = context.socket(self._sock_type)

        host, port = self._host, self._port
        
        if self._bind:
            if port:
                self._socket.bind('tcp://%s:%s' % (host, port))
            else:
                port = self._socket.bind_to_random_port('tcp://%s' % host)
                self._port = port
        else:
            self._socket.connect('tcp://%s:%s' % (host, port))
        self._loop = IOLoop.instance()

    def _parse_address(self, address):
        """ splits the address into host and port (if port is given) """
        if isinstance(address, str):
            address = address.split(':')
        host, port = address if len(address) == 2 else (address[0], None)
        return host, port
        
    def run(self):
        self._setup()
        self._stream = ZMQStream(self._socket)
        self._stream.on_recv(self._messagehandler)

        try:
            self._loop.start()
        except KeyboardInterrupt:
            pass

    @abc.abstractmethod
    def _messagehandler(self, message):
        """ Needs a concrete implementation of how to handle messages """
        return

    def _doc_to_json(self, message):
        """ returns a json object from the message """
        sender, feed_type, payload = msg[:]
        payload = to_json(payload)
        return sender, feed_type, payload
