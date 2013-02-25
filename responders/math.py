from responders import Responder

from sympy.parsing.sympy_parser import parse_expr
import exceptions

class MathResponder(Responder):
    def support(self, message):
        return message[0:4] == 'math'

    def generate(self, message):

        try:
            return "\t%s\n\t=> %s" % (message[5:], float(parse_expr(message[5:])))
        except exceptions.Exception, e:
            return "Parse error: %s" % e.message