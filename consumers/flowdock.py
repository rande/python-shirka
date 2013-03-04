
import requests, twistedhttpstream, exceptions
from twisted.internet import reactor
from consumers import Request, User
import markdown
import unittest
import traceback

from responders import Responder, Response, StreamResponse

class StreamAssistant(object):
    def __init__(self, consumer):
        self.consumer = consumer

    def add(self, response, request):
        def start_responder(response, request, consumer):
            response.handle(request, consumer)
        
        reactor.callInThread(start_responder, response, request, self.consumer)

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
            self.handle_response(responder.on_start(self), Request('on_start', User(None, None, 0), 'init', 'flowdock'))

    def connectionFailed(self, why):
        print "cannot connect:", why
        reactor.stop()

    def create_request(self, message):
        return Request(message['content'], User(None, None, int(message['user'])), message['event'], 'flowdock')

    def messageReceived(self, message):

        request = self.create_request(message)

        if request.user.id == 0:
            return

        if request.type == 'message':
            print u"<<< Request: %s" % request

            for responder in self.responders:
                if not responder.support(request):
                    continue

                print u"    Found responder: %s" % responder

                try:
                    response = responder.generate(request)
                except exceptions.Exception, e:
                    print "!!! Error while handling message:\n\t %s" % e.message

                    return 
                    # raise e

                self.handle_response(response, request)

    def handle_response(self, response, request):
        if isinstance(response, StreamResponse):
            self.stream_assistant.add(response, request)
        else:
            self.post(response, request)

    def normalize(self, response, request):
        if response == False:
            return

        if isinstance(response, (dict)):
            r = Response(response['content'])

            if 'tags' in response:
                r.tags = response['tags']

            response = r

        if not isinstance(response, Response):
            response = Response(response)

        response.command = request.content

        return response

    def markdown(self, content):
        return markdown.markdown(content,  extensions=['headerid(level=3)', 'nl2br', 'tables'])

    def post(self, response, request):
        response = self.normalize(response, request)

        if response in [False, None]:
            return

        print u">>> Response: %s" % response

        if len(response.content) > 300:
            requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
                "content": "\t response too long, check the flowdock inbox!",
                "external_user_name": self.bot.name,
                "tags":  response.tags
            })

            self.flowdock.post(self.bot.email, "Response to %s" % response.command, self.markdown(response.content) , from_name=self.bot.name)    
        else:
            requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
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

