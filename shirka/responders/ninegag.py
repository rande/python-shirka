# vim: set fileencoding=utf-8 :

from shirka.responders import Responder
from random import randint
import requests
from shirka.consumers import BaseTestCase

class NineGagResponder(Responder):  
    def name(self):
        return '9gag'

    def generate(self, request):
        """
        usage: 9gag
        retrieves a random 9gag image
        """
        section = requests.get("http://infinigag.eu01.aws.af.cm/?section=hot").json()

        return section['data'][randint(0, len(section['data']))]['images']['small']

class TestNineGagResponder(BaseTestCase):
    def setUp(self):
        self.responder = NineGagResponder()

    def test_support(self):
        self.assertTrue(self.responder.support(self.create_request("9gag")))
        self.assertFalse(self.responder.support(self.create_request("fuu")))

    def test_valid(self):
        self.assertIsNotNone(self.generate("9gag"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))
