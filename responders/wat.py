# vim: set fileencoding=utf-8 :

from responders import Responder
import requests
import json
import consumers

class WatResponder(Responder):

    def name(self):
        return 'wat'

    def generate(self, request):
        """
        usage: wat
        return a wat image
        """
        r = requests.get('http://watme.herokuapp.com/random').json()

        return r['wat']

class TestWatResponder(consumers.BaseTestCase):
    def setUp(self):
        self.responder = WatResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("wat"))
        self.assertFalse(self.responder.support("fuu"))

    def test_valid(self):
        self.assertIsNotNone(self.generate("wat"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))
