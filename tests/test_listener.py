#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import json
from zmq.utils import jsonapi

from majordomo.utils import to_json

# server side
def get_messages():
    """ listens to a port """
    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect('tcp://127.0.0.1:6000')

    while True:
        try:
            msg = to_json(socket.recv_json())
            print msg
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    get_messages()
