# vim: set fileencoding=utf-8 :

from shirka.consumers import Request, User, StreamAssistant, Consumer
from shirka.responders import Responder, Response, StreamResponse

from twisted.internet import reactor

import requests, twistedhttpstream, exceptions, logging
import markdown, unittest, re

class FlowDockConsumer(twistedhttpstream.MessageReceiver, Consumer):

    def __init__(self, bot, token, responders, flowdock, logger=None):
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
        if not logger:
            self.logger = logging.getLogger('consumers.flowdock')
        else:
            self.logger = logger

    def connectionMade(self):
        self.logger.info("Connection made to flowdock")
        for responder in self.responders:
            self.handle_response(responder.on_start(self), Request('on_start', User(None, None, 0), 'init', 'flowdock'))

    def create_request(self, message):
        if message['event'] == 'comment':
            text = message['content']['text']
        elif message['event'] == 'message':
            text = message['content']
        else:
            return False

        return Request(text, User(None, None, int(message['user'])), message['event'], 'flowdock')

    def messageReceived(self, message):
        request = self.create_request(message)
        
        if not request or request.user.id == 0:
            return

        if request.type == 'message' or request.type == 'comment':
            self.logger.debug("<<< Request: %s" % request.content)

        responses = self.handle_message(request)

        for response in responses:
            self.handle_response(response, request)

    def handle_message(self, request):
        responses = []
        for responder in self.responders:
            if not responder.support(request):
                continue

            self.logger.debug("    Found responder: %s" % responder)

            responses.append(self.normalize(responder.generate(request), request))

        return responses

    def handle_response(self, response, request):
        if isinstance(response, StreamResponse):
            self.stream_assistant.add(response, request)
        else:
            self.post(response, request)


    def post(self, response, request):
        if response in [False, None]:
            return

        self.logger.debug(">>> Response: %s" % response)

        if len(response.content) > 300:
            requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
                "content": "\t response too long, check the flowdock inbox!",
                "external_user_name": self.bot.name,
                "tags":  response.tags
            })

            self.flowdock.post(self.bot.email, "Response to %s" % response.command, self.markdown(response.content) , from_name=self.bot.name)    
        else:
            requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
                "content": self.format(response.content),
                "external_user_name": self.bot.name,
                "tags":  response.tags
            })

class TestFlowDockConsumer(unittest.TestCase):
    def setUp(self):
        from shirka.consumers import Bot
        # from flowdock import FlowDock

        # f = FlowDock(api_key="fake", app_name='Bot %s' % bot.name, project="Project %s" % flow)

        self.consumer = FlowDockConsumer(Bot("name", "email", None), "token", [], None)

    def test_markdown(self):
        help = "# help\n\n##command \n\nusage: help\n"

        expected ="""\
<h3 id="help">help</h3>
<h4 id="command">command</h4>
<p>usage: help</p>\
"""
        self.assertEquals(self.consumer.markdown(help), expected)

    def test_formatter(self):
        message = """\
 > Hello!
 > Bonjour!
 > Holla!\
"""

        expected = """\
\t > Hello!
\t > Bonjour!
\t > Holla!\
"""

        self.assertEquals(self.consumer.format(message), expected)
        self.assertEquals(self.consumer.format("http://foo/my.png"), "http://foo/my.png")
        self.assertEquals(self.consumer.format("https://foo/my.png"), "https://foo/my.png")
        self.assertEquals(self.consumer.format("https://foo/my.tiff"), "\thttps://foo/my.tiff")

        
