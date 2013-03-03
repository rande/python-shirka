
import requests
import twistedhttpstream
import exceptions
import threading
from twisted.internet import reactor

from responders import Responder, Response, StreamResponse

class StreamAssistant(object):
    def __init__(self, consumer):
        # self.responses = []
        self.consumer = consumer

    def add(self, response):
        # self.responses.append(response)
        self.start(response)

    def start(self, response):
        def start_responder(response, consumer):
            response.handle(consumer)
        
        reactor.callInThread(start_responder, response, self.consumer)

class FlowDockConsumer(twistedhttpstream.MessageReceiver):

    def __init__(self, name, token, responders):
        """consumer(responders)

        name - the bot name
        token - the user token
        responders - a set of responders
        """
        self.responders = responders
        self.name = name
        self.token = token
        self.stream_assistant = StreamAssistant(self)

    def connectionMade(self):
        self.post({
            'content': "\tHello, I am a bot! (dev mode)\n\tYou can improve my soul here: https://github.com/rande/nono-le-robot !",
        })

    def connectionFailed(self, why):
        print "cannot connect:", why
        reactor.stop()

    def normalize(self, response):
        if response == False:
            return False

        if not isinstance(response, (Response)):
            response = Response(response)

        return response

    def messageReceived(self, message):
        if u'from' in message['content'] and message['content']['from']['name'] == self.name:
            return

        if 'external_user_name' in message and message['external_user_name'] == self.name:
            return

        if message['event'] == 'message':
            # self.flowdock.post("no-reply@ekino.com", "New message from %s" % message['user'], message['content'], "nono")

            print "Message: %s" % message

            for responder in self.responders:
                if not responder.support(message['content']):
                    continue

                print "Found responder: %s" % responder

                try:
                    response = responder.generate(message['content'])
                except exceptions.Exception, e:
                    return "\tError while handling message:\n\t %s" % e.message

                if isinstance(response, StreamResponse):
                    self.stream_assistant.add(response)
                else:
                    self.post(response)

    def normalize(self, response):
        if response == False:
            return

        if isinstance(response, (dict)):
            r = Response(response['content'])

            if 'tags' in response:
                r.tags = response['tags']

            return r

        if not isinstance(response, Response):
            return Response(response)

        return response

    def post(self, response):
        response = self.normalize(response)

        if response in [False, None]:
            return

        print "send response: %s" % response

        r = requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
            "content": response.content,
            "external_user_name": self.name,
            "tags":  response.tags
        })

        print r
