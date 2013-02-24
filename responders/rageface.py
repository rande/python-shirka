from responders import Responder

class RagefaceResponder(Responder):
    IMG = {
        "troll": "http://fuuu.us/86.png",
        "lol": "http://fuuu.us/176.png",
        "sir": "http://fuuu.us/389.png",
        "fuuu": "http://fuuu.us/217.png",
        "true": "http://fuuu.us/285.png",
        "cute": "http://fuuu.us/447.png",
        "win": "http://fuuu.us/188.png",
    }

    def support(self, message):
        return message[0:4] == 'face'

    def generate(self, message):
        words = message.split(" ")

        if words[1] == 'help':
            return "Face available: %s" % (", ".join(RagefaceResponder.IMG))

        if words[1] in RagefaceResponder.IMG:
            return RagefaceResponder.IMG[words[1]]

        return False