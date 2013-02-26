from responders import Responder

class BigbroResponder(Responder):
    def support(self, message):
        return message[0:2] == 'pt'

    def generate(self, message):
        words = message.split(" ")

        if words[1] == 'help':
            return "pt pseudo message"

        return {
                'content': "\t\t1 point %s pour %s\n" % (words[1], words[2]),
            }

        return False