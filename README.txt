======
Shirka
======

This a bot based on twisted, mostly a python learning project

Consumers
=========

* flowdock: read message from flow dock stream API
* stdin: read message from the cli (testing only)

Responders
==========

* face
* whois
* math
* wat
* xkcd
* ascii
* 9gag
* jira

Installation
============

    virtualenv shirka 
    cd shirka
    source bin/activate
    
    pip install shirka
    python -m shirka --destination bot
    
Usage
=====

    cd bot
    python start.py shirka:start

Running Tests
=============

.. code-block:: python

    python tests.py # run all tests
    python -m unittest responders.xkcd # run one test
