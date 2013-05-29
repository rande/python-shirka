# vim: set fileencoding=utf-8 :

from shirka.responders import Responder
from shirka.consumers import BaseTestCase

DEFAULT_IMG = {
    "awesome":    "http://i.imgur.com/5zKXz.gif",
    "jira":       "http://i.imgur.com/Zjwo4.gif",
    "shame":      "http://i.imgur.com/GVDjO.gif",
    "flag":       "http://i.imgur.com/oN1Er.gif",
    "crazy":      "http://i188.photobucket.com/albums/z284/oblongman7/Scrubs/b6488ee3.gif",
    "notme":      "http://i.imgur.com/V9MavVa.gif",
    "desperate":  "http://media.tumblr.com/tumblr_lsdhbmlL611qhjgo1.gif",
    "waiting":    "http://i.imgur.com/aJaBc.gif",
    "success":    "http://i.imgur.com/AKtqu.gif",
    "dubious":    "http://i.imgur.com/qX3nQi1.gif",
    "baddone":    "http://i.imgur.com/LaOykFc.gif",
    "incredible": "http://i.imgur.com/D26gL.gif",
    "deploy":     "http://i1.kym-cdn.com/photos/images/original/000/234/786/bf7.gif"

}

class SoResponder(Responder):
    def __init__(self, imgs=DEFAULT_IMG):
        self.imgs = imgs

    def name(self):
        return 'so'

    def generate(self, request):
        """
        usage: so [mood] : display the related image
               so help : display available moods
        """
        words = request.content.split(" ")

        if len(words) < 2:
            return False

        if words[1] == 'help':
            return "Moods available: %s" % (", ".join(self.imgs))

        if words[1] in self.imgs:
            return self.imgs[words[1]]

        return "so fail!!!"


class TestSoResponder(BaseTestCase):
    def setUp(self):
        self.responder = SoResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("so"))
        self.assertFalse(self.responder.support("crap"))

    def test_incomplete_command(self):
        self.assertFalse(self.generate("so"))

    def test_help(self):
        self.assertIsNotNone(self.generate("so help"))

    def test_valid(self):
        self.assertEquals(self.generate("so awesome"), "http://i.imgur.com/5zKXz.gif")

    def test_unavailable_mood(self):
        self.assertEquals(self.generate("so crap"), "so fail!!!")

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))

