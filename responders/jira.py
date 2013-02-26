from responders import Responder

class JiraResponder(Responder):
    def support(self, message):
        return message[0:4] == 'jira'

    def generate(self, message):
        words = message.split(" ")

        return "%s va t'occuper de tes Jira" % (words[1])
