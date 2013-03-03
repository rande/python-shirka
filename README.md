Nono le robot
=============

This is a POC a bot with twisted, mostly a self python learning project

### Consumers

 - flowdock: read message from flow dock stream API

### Responders

 - face
 - whois
 - math
 - wat
 - xkcd
 - ascii
 - 9gag

## Installation

Install dependencies

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

## Running Tests

    python -m unittest test # run all tests
    python -m unittest responders.xkcd # run one test

## Usage

```python

import twistedhttpstream
from twisted.internet import reactor
import yaml

from flowdock import FlowDock

from responders import  (
    RagefaceResponder, FlowdockWhoisResponder, MathResponder,  
    XkcdResponder, WatResponder, BigbroResponder, 
    NineGagResponder, LinkResponder, ReminderResponder,
    StatusResponder, HelpResponder
)

from consumers import FlowDockConsumer, Bot

config = yaml.load(file('config.yml', 'r'))

print config

bot = Bot(config['bot']['name'], config['bot']['email'])

responders_collection = {
    'test': [
        StatusResponder(),
        RagefaceResponder(), 
        FlowdockWhoisResponder(
            config['channels']['test']['flowdock']['organisation'], 
            config['channels']['test']['flowdock']['flow']['name'], 
            config['channels']['test']['flowdock']['user']['token']
        ),
        MathResponder(),
        XkcdResponder(),
        WatResponder(),
        BigbroResponder(),
        NineGagResponder(),
        ReminderResponder(),
        HelpResponder(),
    ]
}

if __name__ == "__main__":
    for flow, responders in responders_collection.iteritems():
        channel_config = config['channels'][flow]

        if not config['channels'][flow]['enabled']:
            continue

        url   = "https://stream.flowdock.com/flows/%s/%s" % (channel_config['flowdock']['organisation'], flow)

        f = FlowDock(api_key=channel_config['flowdock']['flow']['token'], app_name='Bot %s' % bot.name, project="Project %s" % flow)

        twistedhttpstream.stream(
            reactor, url, FlowDockConsumer(bot, channel_config['flowdock']['flow']['token'], responders, f), username=channel_config['flowdock']['user']['token'], password=""
        )
    

    reactor.run()

```