Nono le robot
=============

This is a POC a bot with twisted, mostly a self python learning project

### Consumers

 - flowdock: read message from flow dock stream API

### Responders
 
 - face
 - whois
 - math



## Installation

Install dependencies

    pip install twisted
    pip install twistedhttpstream
    pip install requests
    pip install sympy
    pip install pyopenssl
    
## Usage

```python
import twistedhttpstream
from twisted.internet import reactor

#from flowdock import FlowDock

from responders import RagefaceResponder, FlowdockWhoisResponder
from consumers import FlowDockConsumer

# configure
organisation = 'ORGANISATION'
flow         = 'FLOW'
user_token   = 'USER_FLOWDOCK_TOKEN'
flow_token   = 'FLOW_FLOWDOCK_TOKEN'
url          = "https://stream.flowdock.com/flows/%s/%s" % (organisation, flow)
        
if __name__ == "__main__":
    
    responders = [
        RagefaceResponder(), 
        FlowdockWhoisResponder(organisation, flow, user_token)
    ]

    twistedhttpstream.stream(reactor, url, FlowDockConsumer('nono', flow_token, responders), username=user_token, password="")
    reactor.run()

```