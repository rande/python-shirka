from responders import Responder
from random import randint
import requests
import unittest

class NineGagResponder(Responder):  
    def name(self):
        return '9gag'

    def generate(self, message):
        """
        usage: 9gag
        retrieves a random 9gag image
        """
        section = requests.get("http://infinigag.eu01.aws.af.cm/?section=hot").json()

        return section['images'][randint(0, len(section['images']))]['image']['small']

class TestNineGagResponder(unittest.TestCase):
    def setUp(self):
        self.responder = NineGagResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("9gag"))
        self.assertFalse(self.responder.support("fuu"))

    def test_valid(self):
        self.assertIsNotNone(self.responder.generate("9gag"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))
