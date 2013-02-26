from responders import Responder
from random import randint
import urllib2
import json


class NineGagResponder(Responder):  
    def support(self, message):
        return message[0:4] == '9gag' and len(message) == 4

    def generate(self, message):
        node = json.load(urllib2.urlopen("http://infinigag.eu01.aws.af.cm/?section=hot"))['images']
        nbImages = 0

        for image in node: nbImages += 1

        return node[randint(0, nbImages)]['image']['small']