# vim: set fileencoding=utf-8 :

from shirka.responders import Responder
from shirka.consumers import BaseTestCase
from jira.client import JIRA
from jira.resources import dict2resource
from mocker import Mocker
import re

class JiraResponder(Responder):
    def __init__(self, configs, logger=None):
        self.configs = configs
        self.logger = logger

    def name(self):
        return "jira"

    def support(self, request):
        return True

    def generate(self, request):

        message = ""

        for ereg, config in self.configs.iteritems():
            for result in re.finditer(ereg, request.content):
                for key in result.groupdict():
                    if key == "ID":

                        jira  = config['jira']
                        issue = jira.issue(result.groupdict()[key])

                        message = message + "-> " + config['baseUrl'] + result.groupdict()[key] +\
                                  " - " + issue.fields.issuetype.name + " (" + issue.fields.priority.name + ")\n   " +\
                                  issue.fields.summary + "\n   reported by " + issue.fields.reporter.displayName +\
                                  ", assigned to " + issue.fields.assignee.displayName + " - " + issue.fields.status.name +\
                                  " (" + issue.fields.resolution.name + ")\n"

        if len(message) > 0:
            return message

        return False


class TestJiraResponder(BaseTestCase):
    def setUp(self):
        mocker = Mocker()
        jira = mocker.mock()

        jira.issue("SHIRKA-123")
        issue=dict2resource({'fields': {
            'issuetype':  {'name': 'bug'},
            'priority':   {'name': 'major'},
            'summary':    'crappy bug',
            'reporter':   {'displayName': 'John Doe'},
            'assignee':   {'displayName': 'Jane Doe'},
            'status':     {'name': 'Open'},
            'resolution': {'name': 'none'}
        }})
        mocker.result(issue)

        jira.issue("SHIRKA-456")
        issue=dict2resource({'fields': {
            'issuetype':  {'name': 'improvement'},
            'priority':   {'name': 'minor'},
            'summary':    'cool improvement',
            'reporter':   {'displayName': 'Marc Jackson'},
            'assignee':   {'displayName': 'Lynn Liu'},
            'status':     {'name': 'Closed'},
            'resolution': {'name': 'none'}
        }})
        mocker.result(issue)

        jira.issue("SHIRKA-789")
        issue=dict2resource({'fields': {
            'issuetype':  {'name': 'bug'},
            'priority':   {'name': 'blocker'},
            'summary':    'Fix it ASAP!',
            'reporter':   {'displayName': 'Captain Spok'},
            'assignee':   {'displayName': 'Electra'},
            'status':     {'name': 'Open'},
            'resolution': {'name': 'fixed'}
        }})
        mocker.result(issue)

        mocker.replay()
        self.responder = JiraResponder(configs={'(?P<ID>SHIRKA-[0-9]+)': {
            'jira':    jira,
            'baseUrl': 'http//testing.jira.net'
        }})

    def test_support(self):
        self.assertTrue(self.responder.support("SHIRKA-12"))
        self.assertTrue(self.responder.support("whatever"))

    def test_valid(self):
        self.assertEquals("-> http//testing.jira.netSHIRKA-123 - bug (major)\n   " +\
                          "crappy bug\n   reported by John Doe, assigned to Jane Doe - Open (none)\n",
                          self.generate("see SHIRKA-123"))
        self.assertEquals("-> http//testing.jira.netSHIRKA-456 - improvement (minor)\n   " +\
                          "cool improvement\n   reported by Marc Jackson, assigned to Lynn Liu - Closed (none)\n" +\
                          "-> http//testing.jira.netSHIRKA-789 - bug (blocker)\n   " +\
                          "Fix it ASAP!\n   reported by Captain Spok, assigned to Electra - Open (fixed)\n",
                          self.generate("see SHIRKA-456 and SHIRKA-789"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))
