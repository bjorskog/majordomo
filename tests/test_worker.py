#!/usr/bin/env python
# -*- coding: utf-8 -*-

import zmq
import json
import random
import time
import sys
import datetime

#client side
def push_messages(workernum):
    """ generates rngs and pushes """

    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    
    name = "worker%i" % workernum
    print "Starting %s." % name
    socket.setsockopt(zmq.IDENTITY, name)
    socket.connect('tcp://127.0.0.1:5000')
    #socket.bind('tcp://127.0.0.1:5000')

    while True:
        try:
            msg = json.dumps({'worker': name, 'feed': random.random(), 
                              'timestamp':str(datetime.datetime.now())})
            socket.send_multipart(['data.fundamental', msg])
        except KeyboardInterrupt:
            print "Stopping %s..." % name
            break
        time.sleep(random.random()/100.0)

if __name__ == "__main__":
    if len(sys.argv)<2:
        workernum = random.randint(1, 100)
    else:
        workernum = int(sys.argv[1])
    push_messages(workernum)
