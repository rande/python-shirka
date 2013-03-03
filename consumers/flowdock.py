
import requests
import twistedhttpstream
import exceptions
import threading
from twisted.internet import reactor
import markdown
import unittest

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

    def __init__(self, bot, token, responders, flowdock):
        """consumer(responders)

        bot - the bot 
        token - the user token
        responders - a set of responders
        """
        self.responders = responders
        self.bot = bot
        self.token = token
        self.stream_assistant = StreamAssistant(self)
        self.flowdock = flowdock

    def connectionMade(self):
        for responder in self.responders:
            self.handle_response(responder.on_start(self), {'content': 'on_start'})

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

        if 'external_user_name' in message:
            return

        # if u'from' in message['content'] and message['content']['from']['name'] == self.name:
        #     return

        # if 'external_user_name' in message and message['external_user_name'] == self.name:
        #     return

        if message['event'] == 'message':
            print "Message: %s" % message

            for responder in self.responders:
                if not responder.support(message['content']):
                    continue

                print "Found responder: %s" % responder

                try:
                    response = responder.generate(message['content'])
                except exceptions.Exception, e:
                    return "\tError while handling message:\n\t %s" % e.message

                self.handle_response(response, message)

    def handle_response(self, response, message):
        if isinstance(response, StreamResponse):
            self.stream_assistant.add(response, message)
        else:
            self.post(response, message)

    def normalize(self, response, message):
        if response == False:
            return

        if isinstance(response, (dict)):
            r = Response(response['content'])

            if 'tags' in response:
                r.tags = response['tags']

            return r

        if not isinstance(response, Response):
            response = Response(response)

        response.command = message['content']

        return response

    def markdown(self, content):
        return markdown.markdown(content,  extensions=['headerid(level=3)', 'nl2br', 'tables'])

    def post(self, response, message):
        response = self.normalize(response, message)

        if response in [False, None]:
            return

        print "send response: %s" % response

        if len(response.content) > 100:
            r = requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
                "content": "\t response too long, check the flowdock inbox!",
                "external_user_name": self.bot.name,
                "tags":  response.tags
            })

            self.flowdock.post(self.bot.email, "Response to %s" % response.command, self.markdown(response.content) , from_name=self.bot.name)    
        else:
            r = requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
                "content": response.content,
                "external_user_name": self.bot.name,
                "tags":  response.tags
            })

class TestFlowDockConsumer(unittest.TestCase):
    def setUp(self):
        from consumers import Bot
        # from flowdock import FlowDock

        # f = FlowDock(api_key="fake", app_name='Bot %s' % bot.name, project="Project %s" % flow)

        self.consumer = FlowDockConsumer(Bot("name", "email"), "token", [], None)

    def test_markdown(self):
        help = "# help\n\n##command \n\nusage: help\n"

        expected ="""\
<h3 id="help">help</h3>
<h4 id="command">command</h4>
<p>usage: help</p>\
"""
        self.assertEquals(self.consumer.markdown(help), expected)

