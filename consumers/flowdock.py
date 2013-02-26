
import requests
import twistedhttpstream

class FlowDockConsumer(twistedhttpstream.MessageReceiver):

    def __init__(self, name, token, responders):
        """consumer(responders)

        name - the bot name
        token - the user token
        responders - a set of responders
        """
        self.responders = responders
        self.name = name
        self.token = token

    def connectionMade(self):
        self.post({
            'content': "\tHello, I am a bot!\n\tYou can improve my soul here: https://github.com/rande/nono-le-robot !",
        })

    def connectionFailed(self, why):
        print "cannot connect:", why
        reactor.stop()

    def normalize(self, response):

        if response == False:
            return False

        if not isinstance(response, (dict)):
            return {
                'content': response,
                'tags': []
            }

        if 'tags' not in response:
            response['tags'] = []

        if 'content' not in response:
            return False

        return response

    def messageReceived(self, message):
        if u'from' in message['content'] and message['content']['from']['name'] == self.name:
            return

        if 'external_user_name' in message and message['external_user_name'] == self.name:
            return

        if message['event'] == 'message':
            # self.flowdock.post("no-reply@ekino.com", "New message from %s" % message['user'], message['content'], "nono")

            print "Message: %s" % message

            for responder in self.responders:
                if not responder.support(message['content']):
                    continue

                print "Found responder: %s" % responder

                self.post(responder.generate(message['content']))

    def post(self, response):

        response = self.normalize(response)

        if response == False:
            return

        print "send response: %s" % response
        r = requests.post("https://api.flowdock.com/v1/messages/chat/%s" % self.token, data= {
            "content": response['content'],
            "external_user_name": self.name,
            "tags":  response['tags']
        })

        print r
