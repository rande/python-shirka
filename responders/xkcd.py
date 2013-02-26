from responders import Responder
import requests
import json

class XkcdResponder(Responder):

    def support(self, message):
        return message[0:4] == 'xkcd'

    def generate(self, message):
        r = requests.get('http://xkcd.com/%s/info.0.json' % message[5:]).json
        return "%s" % r['img']
