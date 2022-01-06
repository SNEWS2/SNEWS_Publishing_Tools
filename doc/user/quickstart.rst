==========
Quickstart
==========

.. contents::
   :local:


Run SNEWS 2.0
-------------

After installing the module, the command that does the magic is:

.. code:: bash

    snews model

The two required options are:

    * -f: the .env file for required environment variables.
    * --no-auth: True to use the default .toml file. Otherwise, use Hopskotch authentication in the .env file.

So an example command would be

.. code::

     snews model --env-file config.env --no-auth

Configuration
^^^^^^^^^^^^^^

The user should create a .env file and pass the file path to the -f
option when running SNEWS 2.0. The .env file should include the following:

.. code:: python
    COINCIDENCE_THRESHOLD=
    MSG_EXPIRATION=
    TIME_STRING_FORMAT=
    DATABASE_SERVER=
    NEW_DATABASE=
    OBSERVATION_TOPIC=
    TESTING_TOPIC=
    HEARTBEAT_TOPIC=
    ALERT_TOPIC=

The definition of these environmental variables are:
    * COINCIDENCE_THRESHOLD: maximum time (s) between messages for them to be considered coincident
    * MSG_EXPIRATION: maximum time (s) that a message will be stored in the database cache before expiring
    * TIME_STRING_FORMAT: the string format of time in all SNEWS messages.
    * DATABASE_SERVER: the database server to that SNEWS 2.0 connects to in order to store messages for processing. In the current version, the app takes in a **MongoDB** server.
    * NEW_DATABASE: "True" to drop all previous messages and "False" to keep them.
    * OBSERVATION_TOPIC: the Hopskotch topic for detectors to publish messages to.
    * TESTING_TOPIC: the optional topic for testing.
    * ALERT_TOPIC: the Hopskotch topic for SNEWS 2.0 to publish alert messages to the detectors.

Access to Hopskotch
^^^^^^^^^^^^^^^^^^^

To configure a .toml file for hop-client module, follow the steps documented
at https://github.com/scimma/hop-client and specify --default-authentiation as False.

Otherwise, in the .env file, include the following:

.. code:: python

    USERNAME=username
    PASSWORD=password

where "username" and "password" are user credentials to Hopsckoth.


Generate Messages
^^^^^^^^^^^^^^^^^^

:code:`snews generate` can be used to simulate real-time messages from experiments:

.. code:: bash

    snews generate

with options

    * --env-file: the .env file for configuration.
    * --rate: the rate of messages sent in seconds (e.g. 2 means one message every 2 seconds).
    * --alert-probability: the discrete probability that the message is significant.
    * --persist: continually send messages. If not specified, send only one message.

For example, to continuously publish two messages per second, each with a 10% probability of being a significant, enter:

.. code:: bash

    snews generate --env-file config.env --rate 0.5 --alert-probability 0.1


Alternative Instances
^^^^^^^^^^^^^^^^^^^^^^

If the user does not have access to the Hopskotch or MongoDB server or both,
running local instances is a alternative choice.

* To run a Kafka instance, run the following in the shell

.. code:: bash

    docker run -p 9092:9092 -it --rm --hostname localhost scimma/server:latest --noSecurity

and pass the following Kafka server to SNEWS 2.0

.. code:: python

    kafka://dev.hop.scimma.org:9092/USER-TOPIC

* To run a MongoDB instance, either run

.. code:: bash

    docker run -p 27017:27017 -it --rm --hostname localhost mongo:latest

or run

.. code:: bash

    pip install -U mongoengine

and pass the following MongoDB server to SNEWS 2.0

.. code::

    mongodb://localhost:27017/
