from responders import Responder
import unittest

class BigbroResponder(Responder):
    def name(self):
        return 'pt'

    def generate(self, message):
        """
        usage: pt user message
        Generate a point to the provided user
        """
        words = message.split(" ")

        if words[1] == 'help':
            return "pt pseudo message"

        if len(words) < 3:
            return False

        return {
            'content': "\t\t1 point %s pour %s\n" % (words[1], words[2]),
            'tags': ['#bigbro']
        }

        return False

class TestBigbroResponder(unittest.TestCase):
    def setUp(self):
        self.responder = BigbroResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("pt"))
        self.assertFalse(self.responder.support("fuu"))

    def test_help(self):
        self.assertEquals(self.responder.generate("pt help"), "pt pseudo message")

    def test_invalid_count(self):
        self.assertFalse(self.responder.generate("pt salut"))

    def test_valid(self):
        self.assertEquals(self.responder.generate("pt cool rande"), {'content': '\t\t1 point cool pour rande\n', 'tags': ['#bigbro']})

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))

