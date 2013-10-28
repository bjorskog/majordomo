#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import json
import datetime

class TestSocket(object):
     def __init__(self, context, sock_type, name):
         self._context = context
         self._sock = context.socket(sock_type)
         self._sock.setsockopt(zmq.IDENTITY, name)

     def connect(self, *args, **kwargs):
         return self._sock.connect(*args, **kwargs)

     def send(self, message):
         return self._sock.send_multipart(message)

     def recv(self, *args, **kwargs):
         for i in range(100):
             try:
                 rep = req_sock.recv(zmq.NOBLOCK)
                 break
             except:
                 import time; time.sleep(0.01)
         else:
             raise zmq.ZMQError('Got no answer.')
         return rep

     def __del__(self):
          self._context.__del__

def test_echo_server():
     """Tests if the echo server responds properly."""
     context = zmq.Context()
     req_sock = TestSocket(context, zmq.PUB, "testsock")
     req_sock.connect('tcp://127.0.0.1:5000')
     req_sock.send(['data.fundamental', json.dumps({'cmd':'feed', 'timestamp':str(datetime.datetime.now())})])

if __name__ == "__main__":
     test_echo_server()
