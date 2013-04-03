# vim: set fileencoding=utf-8 :

from twisted.internet import reactor
from shirka.responders import Response, StreamResponse

import unittest, re, markdown

class Bot(object):
    def __init__(self, name, email, url, process_executor=None):
        self.name = name
        self.email = email
        self.url = url
        self.process_executor = process_executor

class User(object):
    def __init__(self, name, email, id):
        self.name = name
        self.email = email
        self.id = id

    def __repr__(self):
        return self.name

class Request(object):
    def __init__(self, content, user, type, provider):
        self.content = content
        self.user = user
        self.type = type
        self.provider = provider

    def __str__(self):
        return self.content

    def __unicode__(self):
        return self.content

    def __repr__(self):
        return self.content

    def __getitem__(self, key):
        return self.content[key]

class BaseTestCase(unittest.TestCase):
    def create_request(self, message):
        return Request(message, None,  None,  None)

    def generate(self, message):
        return self.responder.generate(self.create_request(message))


class StreamAssistant(object):
    def __init__(self, consumer):
        self.consumer = consumer

    def add(self, response, request):
        reactor.callInThread(response.handle, request, self.consumer)


class Consumer(object):
    def normalize(self, response, request):
        if response == False:
            return

        if isinstance(response, (dict)):
            r = Response(response['content'])

            if 'tags' in response:
                r.tags = response['tags']

            response = r

        if isinstance(response, StreamResponse):
            return response

        if not isinstance(response, Response):
            response = Response(response)

        response.command = request.content

        return response

    def markdown(self, content):
        return markdown.markdown(content,  extensions=['headerid(level=3)', 'nl2br', 'tables'])

    def format(self, content):
        if re.match("(http|https)://(.*)\.(gif|jpg|jpeg|png)", content):
            return content

        return "\t" + "\n\t".join(content.split("\n"))

class TestRequest(BaseTestCase):
    def setUp(self):
        self.request = self.create_request("the content")

    def test_slice(self):
        self.assertEquals("the", self.request[0:3])

    def test_unicode(self):
        self.request = self.create_request(u"étrange...")
        self.assertEquals(u"étrange...", u"%s" % self.request)
        

from flowdock import FlowDockConsumer