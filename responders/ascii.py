from responders import Responder
import requests, re
import unittest

class AsciiResponder(Responder):

    def support(self, message):
        return message[0:5] == 'ascii'

    def generate(self, message):
        payload = {'s': message[6:]}
        ascii = requests.get('http://asciime.heroku.com/generate_ascii', params=payload).text
        
        return re.sub('^|\n', '\n\t', ascii)

class TestAsciiResponder(unittest.TestCase):
    def setUp(self):
        self.responder = AsciiResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("ascii"))
        self.assertFalse(self.responder.support("fuu"))

    def test_valid(self):
        self.assertIsNotNone(self.responder.generate("wat"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))
