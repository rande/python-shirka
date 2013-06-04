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
        self.jira = JIRA()

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

                        self.jira = JIRA(options={'server': config['server']}, basic_auth=config['basic_auth'])

                        issue = self.jira.issue(result.groupdict()[key])

                        resolution = u"n/a"
                        if not (issue.fields.resolution is None):
                            resolution = issue.fields.resolution.name

                        message = u"{0}➜ {1}{2} - {3} ({4})\n  {5}\n  reported by {6}, assigned to {7} - {8} ({9})\n".format(
                            message, config['base_url'], result.groupdict()[key], issue.fields.issuetype.name,
                            issue.fields.priority.name, issue.fields.summary, issue.fields.reporter.displayName,
                            issue.fields.assignee.displayName, issue.fields.status.name, resolution)

        if len(message) > 0:
            return message

        return False


class TestJiraResponder(BaseTestCase):
    def setUp(self):
        mocker = Mocker()
        jiraIssue = mocker.replace("jira.client.JIRA.issue")

        jiraIssue("SHIRKA-123")
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

        jiraIssue("SHIRKA-456")
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

        jiraIssue("SHIRKA-789")
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
            'server':     'http://jira.fake.net',
            'base_url':   'http//testing.jira.net',
            'basic_auth': ['user', 'pwd']
        }})

    def test_support(self):
        self.assertTrue(self.responder.support("SHIRKA-12"))
        self.assertTrue(self.responder.support("whatever"))

    def test_valid(self):
        self.assertEquals(u"➜ http//testing.jira.netSHIRKA-123 - bug (major)\n"
                          u"  crappy bug\n"
                          u"  reported by John Doe, assigned to Jane Doe - Open (none)\n",
                          self.generate("see SHIRKA-123"))
        self.assertEquals(u"➜ http//testing.jira.netSHIRKA-456 - improvement (minor)\n"
                          u"  cool improvement\n"
                          u"  reported by Marc Jackson, assigned to Lynn Liu - Closed (none)\n"
                          u"➜ http//testing.jira.netSHIRKA-789 - bug (blocker)\n"
                          u"  Fix it ASAP!\n"
                          u"  reported by Captain Spok, assigned to Electra - Open (fixed)\n",
                          self.generate("see SHIRKA-456 and SHIRKA-789"))

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))
