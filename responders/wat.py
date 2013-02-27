from responders import Responder
import requests
import json
import unittest

class WatResponder(Responder):

    def support(self, message):
        return message[0:4] == 'wat'

    def generate(self, message):
        r = requests.get('http://watme.herokuapp.com/random').json()

        return r['wat']

class TestWatResponder(unittest.TestCase):
    def setUp(self):
        self.responder = WatResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("wat"))
        self.assertFalse(self.responder.support("fuu"))

    def test_valid(self):
        self.assertIsNotNone(self.responder.generate("wat"))
