# vim: set fileencoding=utf-8 :

from responders import Responder, StreamResponse
import consumers
import requests, time

class StreamMonitorResponse(StreamResponse):
    def __init__(self, servers):
        self.servers = servers
        self.status = {
            'http' : {}
        }
    
    def monitor_http(self):
        if 'http' not in self.servers:
            return

        servers = self.servers['http']

        for key in servers:
            if key not in self.status['http']:
                self.status['http'][key] = {'status': 'unknown', 'retry': 0}

            try:
                requests.get(servers[key]['url'], **servers[key]['options'])
                self.status['http'][key] = {'status': 'ok', 'retry': 0}
            except requests.exceptions.RequestException, e:
                self.status['http'][key]['status'] = 'ko'
                self.status['http'][key]['retry'] = self.status['http'][key]['retry'] + 1

                if self.status['http'][key]['retry'] == 1:
                    consumer.post("Monitor: the server %s fails to response" % servers[key]['url'], request)
                elif self.status['http'][key]['retry'] == 5:
                    consumer.post("Monitor: the server %s fails to response (5 times in a row)" % servers[key]['url'], request)
                elif self.status['http'][key]['retry'] % 1000 == 0:
                    consumer.post("Monitor: the server %s fails to response" % servers[key]['url'], request)

    def handle(self, request, consumer):
        while(1):
            time.sleep(5)
            self.monitor_http()


class MonitorResponder(Responder):
    def __init__(self, servers):
        self.servers = servers
        self.monitor = StreamMonitorResponse(self.servers)
    
    def name(self):
        return 'monitor'

    def on_start(self, consumer):
        return self.monitor

    def generate(self, request):
        """
        usage: monitor
        """

        response = ["# Monitor"]

        response.append("## http")

        for key in self.monitor.status['http']:
            response.append("> %s : %s" % (key, self.monitor.status['http'][key]['status']))

        return "\n".join(response)


class TestMonitorResponder(consumers.BaseTestCase):
    def setUp(self):
        self.responder = MonitorResponder({
            'http': {}
        })

    def test_support(self):
        self.assertTrue(self.responder.support("monitor"))
        self.assertFalse(self.responder.support("fuu"))

    def test_valid(self):
        self.assertEquals("# Monitor\n## http", self.generate("monitor"))

    def test_on_start(self):
        self.assertIsInstance(self.responder.on_start(False), StreamMonitorResponse)
