from responders import Responder
import consumers
import re

class LinkResponder(Responder):
    def __init__(self, links):
        self.links = links

        super(LinkResponder, self).__init__()

    def name(self):
        return "link"

    def support(self, message):
        return True

    def generate(self, request):
        origin = request.content

        for ereg, replace in self.links:
             message = re.sub(ereg, replace, request.content)

        if message == origin:
            return False
            
        return "\t%s" % message

class TestLinkResponder(consumers.BaseTestCase):
    def setUp(self):
        self.responder = LinkResponder([
            (r'( |#)NONO-([0-9]*)', r' http://bug/NONO-\2'),
        ])

    def test_support(self):
        self.assertTrue(self.responder.support("pt"))
        self.assertTrue(self.responder.support("fuu"))

    def test_valid(self):
        self.assertEquals('\tVoir le bug http://bug/NONO-123', self.generate("Voir le bug NONO-123"))
        self.assertEquals('\tVoir le bug http://bug/NONO-123 et http://bug/NONO-124', self.generate("Voir le bug NONO-123 et NONO-124"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))
