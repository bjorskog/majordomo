#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
from zmq.utils import jsonapi

to_json = lambda z: jsonapi.loads(z)

# server side
def get_messages():
    """ listens to a port """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect('tcp://127.0.0.1:5000')
    #socket.bind('tcp://127.0.0.1:5000')
    socket.setsockopt(zmq.SUBSCRIBE, '')

    while True:
        try:
            msg = socket.recv() #_multipart()
            print msg
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    get_messages()
