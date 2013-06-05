# vim: set fileencoding=utf-8 :

from shirka.responders import Responder
from shirka.consumers import BaseTestCase
from mocker import Mocker
import subprocess


class VersionResponder(Responder):
    def __init__(self, bot_name):
        self.bot_name = bot_name

    def name(self):
        return 'version'

    def generate(self, request):
        """
        usage: version
        return current bot version by getting the closest git tag
        """

        version = subprocess.check_output(["git", "describe", "--abbrev=0", "--tags"])

        return "%s - V%s" % (self.bot_name, version)


class TestVersionResponder(BaseTestCase):
    def setUp(self):
        mocker = Mocker()
        git_subprocess = mocker.replace("subprocess.check_output")
        git_subprocess(["git", "describe", "--abbrev=0", "--tags"])
        mocker.result("0.0.1")
        mocker.replay()

        self.responder = VersionResponder("shirka")

    def test_support(self):
        self.assertTrue(self.responder.support(self.create_request("version")))
        self.assertFalse(self.responder.support(self.create_request("fuu")))

    def test_valid(self):
        self.assertEquals("shirka - V0.0.1", self.generate("version"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))