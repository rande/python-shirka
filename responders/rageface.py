from responders import Responder

import unittest

class RagefaceResponder(Responder):
    IMG = {
        "badumtss": "http://fuuu.us/363.png",
        "cerealguy": "http://fuuu.us/144.png",
        "cute": "http://fuuu.us/447.png",
        "deskflip": "http://fuuu.us/217.png",
        "fuckyeah": "http://fuuu.us/12.png",
        "genius": "http://fuuu.us/292.png",
        "itssomething": "http://fuuu.us/408.png",
        "lol": "http://fuuu.us/176.png",
        "longneck": "http://fuuu.us/107.png",
        "megusta": "http://fuuu.us/35.png",
        "notbad": "http://fuuu.us/172.png",
        "nothing": "http://fuuu.us/230.png",
        "pokerface": "http://fuuu.us/268.png",
        "rageguy": "http://fuuu.us/61.png",
        "sir": "http://fuuu.us/389.png",
        "troll": "http://fuuu.us/86.png",
        "true": "http://fuuu.us/285.png",
        "win": "http://fuuu.us/188.png",
    }

    def support(self, message):
        return message[0:4] == 'face'

    def generate(self, message):
        words = message.split(" ")

        if len(words) < 2:
            return False

        if words[1] == 'help':
            return "Face available: %s" % (", ".join(RagefaceResponder.IMG))

        if words[1] in RagefaceResponder.IMG:
            return RagefaceResponder.IMG[words[1]]

        return False


class TestRagefaceResponder(unittest.TestCase):
    def setUp(self):
        self.responder = RagefaceResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("face"))
        self.assertFalse(self.responder.support("fuu"))

    def test_incomplete_command(self):
        self.assertFalse(self.responder.generate("face"))

    def test_help(self):
        self.assertIsNotNone(self.responder.generate("face help"))

    def test_valid(self):
        self.assertEquals(self.responder.generate("face win"), "http://fuuu.us/188.png")

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))

        