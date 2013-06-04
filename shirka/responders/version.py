# vim: set fileencoding=utf-8 :

from shirka.responders import Responder
from shirka.consumers import BaseTestCase
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