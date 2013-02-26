from responders import Responder
import unittest

class BigbroResponder(Responder):
    def support(self, message):
        return message[0:2] == 'pt'

    def generate(self, message):
        words = message.split(" ")

        if words[1] == 'help':
            return "pt pseudo message"

        if len(words) < 3:
            return False

        return {
            'content': "\t\t1 point %s pour %s\n" % (words[1], words[2]),
        }

        return False

class TestMathResponder(unittest.TestCase):
    def setUp(self):
        self.responder = MathResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("pt"))
        self.assertFalse(self.responder.support("fuu"))

    def test_help(self):
        self.assertEquals(self.responder.generate("pt help"), "pt pseudo message")

    def test_invalid_count(self):
        self.assertFalse(self.responder.generate("pt salut"))

    def test_valid(self):
        self.assertEquals(self.responder.generate("pt cool rande"), "\t\t1 point cool pour rande\n")
