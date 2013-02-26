from responders import Responder
import requests
import json
import unittest
import exceptions

class XkcdResponder(Responder):
    def support(self, message):
        return message[0:4] == 'xkcd'

    def generate(self, message):

        try:
            r = requests.get('http://xkcd.com/%s/info.0.json' % message[5:]).json()
        except exceptions.ValueError, e:
            return False

        return r['img']

class TestXkcdResponder(unittest.TestCase):
    def setUp(self):
        self.responder = XkcdResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("xkcd"))
        self.assertFalse(self.responder.support("fuu"))

    def test_valid(self):
        self.assertEquals(self.responder.generate("xkcd 1"), "http://imgs.xkcd.com/comics/barrel_cropped_(1).jpg")

    def test_invalid(self):
        self.assertFalse(self.responder.generate("xkcd fake"))
