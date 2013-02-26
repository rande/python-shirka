from responders import Responder
import requests
import json

class WatResponder(Responder):

    def support(self, message):
        return message[0:4] == 'wat'

    def generate(self, message):
        r = requests.get('http://watme.herokuapp.com/random').json()

        return r['wat']
