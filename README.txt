======
Shirka
======

This a bot based on twisted, mostly a python learning project

Consumers
=========

* flowdock: read message from flow dock stream API

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

Install dependencies::

    pip install twisted
    pip install twistedhttpstream
    pip install requests
    pip install sympy
    pip install mocker
    pip install pyopenssl
    pip install python-flowdock
    pip install markdown
    pip install paramiko
    pip install pyyaml
    pip install ioc
    pip install jira-python

Running Tests
=============

.. code-block:: python

    python tests.py # run all tests
    python -m unittest responders.xkcd # run one test

Usage
=====

- start.py

.. code-block:: python

    # vim: set fileencoding=utf-8 :

    import twistedhttpstream, yaml, sys, logging
    from twisted.internet import reactor
    import ioc

    logging.basicConfig(level=logging.DEBUG)

    container = ioc.build([
        'config.yml',
    ])

    if __name__ == "__main__":

        for flow in container.parameters.get('consumers'):
            if not container.has("consumer.%s.flowdock" % flow):
                continue

            twistedhttpstream.stream(
                container.get('ioc.extra.twisted.reactor'), 
                "https://stream.flowdock.com/flows/%s/%s" % (container.parameters.get("flowdock.%s.organisation" % flow), flow), 
                container.get("consumer.%s.flowdock" % flow), 
                username=container.parameters.get("shirka.flowdock.user.token"),
                password=""
            )
        
        container.get('ioc.extra.twisted.reactor').run()

- Configuration file

.. code-block:: yaml

    shirka:
        data_dir: /path/to/stored/data

    ioc.extra.flask:
    ioc.extra.twisted:

    parameters:
        consumers: [test]
        bot.name: nono
        bot.email: no-reply@shirka.com

        remote.users: [XXX]
        remote.servers: 
            # paramiko option - http://www.lag.net/paramiko/docs/paramiko.SSHClient-class.html
            nono: {host: XXXX, username: XXXX, look_for_keys: false, password: XXXX }

        # configure flow parameterstest
        flowdock.test.organisation: shirka
        flowdock.test.flow.name:    FLOW_NAME
        flowdock.test.flow.token:   FLOW_TOKEN
        flowdock.test.user.name:    rande
        flowdock.test.user.token:   USER_TOKEN

        # jira
        jira.1.server:   https://jira.1.net
        jira.1.base_url: '%jira.1.server%/browse/'
        jira.1.auth:     !!python/tuple [JIRA_USER_1, JIRA_PWD_1]

        jira.2.server:   https://jira.2.net
        jira.2.base_url: '%jira.2.server%/browse/'
        jira.2.auth:     !!python/tuple [JIRA_USER_2, JIRA_PWD_2]


    services:

        # Configure the bot
        bot:
            class: shirka.consumers.Bot
            arguments: [ '%bot.name%', '%bot.email%']

        # Configure shared responders
        responders.math:        { class: shirka.responders.mate.MathResponder }
        responders.xkcd:        { class: shirka.responders.xkcd.XkcdResponder }
        responders.big_bro:     { class: shirka.responders.bigbro.BigbroResponder }
        responders.reminder:    { class: shirka.responders.reminder.ReminderResponder }
        responders.status:      { class: shirka.responders.status.StatusResponder }
        responders.rage_face:   { class: shirka.responders.rageface.RagefaceResponder }
        responders.wat:         { class: shirka.responders.wat.WatResponder }
        responders.9gag:        { class: shirka.responders.ninegag.NineGagResponder }

        responders.remote:
            class: shirka.responders.remote.RemoteResponder
            arguments: 
                - '%remote.servers%'
                - '%remote.users%'


        # Configure flowdock push API
        flowdock.test:
            class: flowdock.FlowDock
            kwargs: 
                api_key:  '%flowdock.test.flow.token%'
                app_name: '%bot.name%'
                project:  Project test

        consumer.test.flowdock.logger:
            class: logging.getLogger
            arguments:
                - 'flowdock.%flowdock.test.flow.name%'

        responders.jira:
            class: shirka.responders.JiraResponder
            arguments:
              - '(?P<ID>JR1-[0-9]+)':
                  server:     '%jira.1.server%'
                  baseUrl:    '%jira.1.base_url%'
                  basic_auth: '%jira.1.auth%'
                '(?P<ID>JR2-[0-9]+)':
                  server:     '%jira.2.server%'
                  baseUrl:    '%jira.2.base_url%'
                  basic_auth: '%jira.2.auth%'
                
        # Configure Stream API Consumer with valid responders
        consumer.test.flowdock:
            class: shirka.consumers.FlowDockConsumer
            arguments: 
                - '@shirka.bot'
                - "%flowdock.test.flow.token%"
                - 
                    - '@responders.rage_face' 
                    - '@responders.test.whois'
                    - '@responders.math' 
                    - '@responders.big_bro'
                    - '@responders.reminder'
                    - '@responders.remote'
                    - '@responders.status'
                    - '@responders.test.help'
                    - '@responders.test.whois'
                    
                - '@flowdock.test'
            kwargs:
                logger: '@consumer.test.flowdock.logger'

        responders.test.whois:
            class: shirka.responders.FlowdockWhoisResponder
            arguments:
                - '%flowdock.test.organisation%'
                - '%flowdock.test.flow.name%'
                - '%flowdock.test.user.token%'

        responders.test.help:
            class: shirka.responders.help.HelpResponder
