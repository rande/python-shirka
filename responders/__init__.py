
class Responder(object):
    def support(message):
        pass

    def generate(message):
        pass

class StreamResponder(Responder):
    def __init__(self):
        self.is_completed = False
        self.messages = []

    def pop(self):
        return self.messages.pop()

    def push(self, message):
        return self.messages.append(message)

    def stop(self):
        self.is_completed = True


from rageface import RagefaceResponder
from flowdock import FlowdockWhoisResponder
from math import MathResponder
from wat import WatResponder
from xkcd import XkcdResponder
from bigbro import BigbroResponder
from ascii import AsciiResponder
from ninegag import NineGagResponder
from link import LinkResponder