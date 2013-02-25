from responders import Responder

class RagefaceResponder(Responder):
    IMG = {
        "troll": "http://fuuu.us/86.png",
        "lol": "http://fuuu.us/176.png",
        "sir": "http://fuuu.us/389.png",
        "deskflip": "http://fuuu.us/217.png",
        "true": "http://fuuu.us/285.png",
        "cute": "http://fuuu.us/447.png",
        "win": "http://fuuu.us/188.png",
        "notbad": "http://fuuu.us/172.png",
        "fuckyeah": "http://fuuu.us/12.png",
        "genius": "http://fuuu.us/292.png",
        "pokerface": "http://fuuu.us/268.png",
        "cerealguy": "http://fuuu.us/144.png",
        "longneck": "http://fuuu.us/107.png",
        "megusta": "http://fuuu.us/35.png",
        "badumtss": "http://fuuu.us/363.png",
        "rageguy": "http://fuuu.us/61.png",
        "nothing": "http://fuuu.us/230.png",
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
