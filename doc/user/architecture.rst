=============
Architecture
=============

The SNEWS 2.0 implementation has three major components:

.. contents::
   :local:



Model
------

The model initializes a Decider object and opens up a kafka stream
through hop-client to read in messages from detectors. The model would
evoke different processing functions depending on the message type. The message
types and corresponding processing algorithms are stored as a mapping in

.. code-block::

    self.mapping = {
            SNEWSObservation.__name__: self.processObservationMessage,
            SNEWSHeartbeat.__name__: self.processHeartbeatMessage
    }

Upon receiving an observation message, it stores the message by calling
methods of the decider and then runs the coincidence requirement check
through the decider's methods. If the deciding function indicates
the possibility of a potential supernova, the model generates an
alert message and sends it to all detectors through a differet Hopskotch
stream.

Each detector are required to periodically send heartbeat messages. The model
keeps a record of which detectors are on or off and removes detectors from which
it has not heard back in a long time. When receiving a heartbeat message,
the model updates the status of status and machine time of the detector included
in this message.


Decider
--------

A decider consists of a Database Storage object and an implementation of the
SNEWS coincidence requirement protocol (the :code:`deciding()` function).

Pseudocode for the deciding protocol logic is:

.. code::
   # check if any messages are in the cache
   if not self.db.cacheEmpty():
     # fetch messages in the cache
     cacheMsgs = self.db.getCacheMsgs()
     # go through cacheMsgs to verify that at least two occur within the coincidence threshold
         # if yes
             # verify that at least two of the locations are different
             # if yes
                 return true
             # if not
                 return false
         # if not, pass


The API of the decider class is defined as

.. code::

    class IDecider(object):
    def deciding(self):
        pass

    def addMessage(self, time, neutrino_time, message):
        pass

    def getAllMessages(self):
        pass


Database Storage
-----------------

This is an object for storing and queueing observation messages
received by the model. In order to support the coincidence requirement
check and future SNEWS usage, the storage object should have the
functionality to received timestamped messages. The API of this class is

.. code:: python

    class IStorage(object):
    def insert(self, time, neutrino_time, message):
        pass

    def getAllMessages(self):
        pass

    def cacheEmpty(self):
        pass

    def getMsgFromStrID(self, post_id):
        pass

For the first release/pre-release of SNEWS 2.0, MongoDB is used
to implement this IStorage interface. TTL indexes are used to expire
messages. Two MongoDB collections are created here, with one storing all messages
and the other one acting as a timed cache for coincidence requirement check.
