==================
SNEWS Protocols
==================

.. contents::
   :local:


Coincidence Requirement
------------------------

Upon observing a potential pre-supernova phenomena, the detector
generates an observation message and publish it. The SNEWS 2.0
server reads in the message and run the coincidence requirement
check defined by SNEWS astronomers. The first version of the
protocol compares the time and locations of observations among
unexpired messages. The simplified version of the algorithm is

.. code-block::

    If there're multiple messages within the last 24 hours:
        Then iterates through messages to check if any two or more are within 10s
            If yes:
                verify locations different (as long as at least two are in different locations)
                    If the locations are different:
                        return true
                    Otherwise:
                        return false
                If not, no-op or print a message
            if no:
                no-op

In future releases, the coincidence requirement protocol
will likely include triangulations to identify coordinates of the
possible supernova.
