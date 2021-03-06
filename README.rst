===============================
majordomo
===============================

.. image:: https://badge.fury.io/py/majordomo.png
    :target: http://badge.fury.io/py/majordomo
    
.. image:: https://travis-ci.org/bjorskog/majordomo.png?branch=master
        :target: https://travis-ci.org/bjorskog/majordomo

.. image:: https://pypip.in/d/majordomo/badge.png
        :target: https://crate.io/packages/majordomo?version=latest


Python package for managing data using ZMQ and MongoDB.

* Free software: BSD license

Features
--------

Writer that pushes all data in the incoming stream to MongoDB.

Building blocks
--------

* Base classes for streams, workers and commands
* Broker class for doing N-N pub-sub.
* Controller for writing to MongoDB
* Workers for obtaining data
* Workflow objects for defining tasks, sources and dependencies
