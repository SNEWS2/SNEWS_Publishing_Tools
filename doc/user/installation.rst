============
Installation
============

.. contents::
   :local:

You can install snews publishing tools via ~pip~ or from source.

.. role:: strike
    :class: strike

:strike: To install with pip:
Currently it is not yet deployed to pip. Please install from the source

.. code:: bash

   :strike: pip install -U snews

To install from source:
Using ssh-key:

.. code:: bash

    git clone git@github.com:SNEWS2/SNEWS_Publishing_Tools.git
    cd SNEWS_Publishing_Tools
    pip install ./ --user

Using HTTPS:

.. code:: bash

    git clone https://github.com/SNEWS2/SNEWS_Publishing_Tools.git
    cd SNEWS_Publishing_Tools
    pip install ./ --user

Using downloaded ZIP file:

.. code:: bash

    tar -xzf SNEWS_Publishing_Tools-main.zip
    cd SNEWS_Publishing_Tools
    pip install ./ --user
