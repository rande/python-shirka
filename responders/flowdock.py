from responders import Responder

import requests

class FlowdockWhoisResponder(Responder):
    def __init__(self, organisation, flow, token):
        """consumer(flowdock)

        flowdock - The flowdock instance
        """
        self.organisation = organisation
        self.flow = flow
        self.token = token

    def support(self, message):
        return message[0:5] == 'whois'

    def generate(self, message):
        words = message.split(" ")

        user = False
        if not words[1].isdigit():
            users = requests.get("https://api.flowdock.com/flows/%s/%s/users" % (self.organisation, self.flow), auth=(self.token, '')).json()

            for u in users:
                if u['nick'] == words[1]:
                    user = u
                    break
        else:
            user = requests.get("https://api.flowdock.com/users/%s" % words[1], auth=(self.token, '')).json()    

        if user:
            return {
                'content': "%s is %s (%s)" % (words[1], user['name'], user['email']),
                'tags': ['#contact']
            }

        return False
        