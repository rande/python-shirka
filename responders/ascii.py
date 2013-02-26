from responders import Responder
import requests, re

class AsciiResponder(Responder):

    def support(self, message):
        return message[0:5] == 'ascii'

    def generate(self, message):
        payload = {'s': message[6:]}
        ascii = requests.get('http://asciime.heroku.com/generate_ascii', params=payload).text
        return re.sub('^|\n', '\n\t', ascii)
