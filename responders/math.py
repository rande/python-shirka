from responders import Responder
from sympy.parsing.sympy_parser import parse_expr
import exceptions
import unittest

class MathResponder(Responder):
    def support(self, message):
        return message[0:4] == 'math'

    def generate(self, message):

        try:
            return "\t%s\n\t=> %s" % (message[5:], float(parse_expr(message[5:])))
        except exceptions.Exception, e:
            return "Parse error: %s" % e.message

class TestMathResponder(unittest.TestCase):
    def setUp(self):
        self.responder = MathResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("math"))
        self.assertFalse(self.responder.support("fuu"))

    def test_valid(self):
        self.assertEquals(self.responder.generate("math 1 + 1"), "\t1 + 1\n\t=> 2.0")
