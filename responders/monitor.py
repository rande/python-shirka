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
    
    def get_http_args(self, options):

        args = {}
        if 'auth' in options:
            args['auth'] = (options['auth'][0], options['auth'][1])
        
        if 'verify' in options:
            args['verify'] = options['verify']

        return args

    def monitor_http(self, request, consumer):
        if 'http' not in self.servers:
            return

        servers = self.servers['http']

        for key in servers:
            if key not in self.status['http']:
                self.status['http'][key] = {'status': 'unknown', 'retry': 0}

            try:
                requests.get(servers[key]['url'], **self.get_http_args(servers[key]['options']))

                if self.status['http'][key]['status'] == 'ko':
                    consumer.post("Monitor: [OK] the server %s - %s is now up!" % (key, servers[key]['url']), request)

                self.status['http'][key] = {'status': 'ok', 'retry': 0}
            except requests.exceptions.RequestException, e:

                print e

                self.status['http'][key]['status'] = 'ko'
                self.status['http'][key]['retry'] = self.status['http'][key]['retry'] + 1

                if self.status['http'][key]['retry'] == 1:
                    consumer.post("Monitor: [KO] the server %s - %s fails to response" % (key, servers[key]['url']), request)
                elif self.status['http'][key]['retry'] == 5:
                    consumer.post("Monitor: [KO] the server %s - %s fails to response (5 times in a row)" % (key, servers[key]['url']), request)
                elif self.status['http'][key]['retry'] % 1000 == 0:
                    consumer.post("Monitor: [KO] the server %s - %s fails to response" % (key, servers[key]['url']), request)

    def handle(self, request, consumer):
        while(1):
            self.monitor_http(request, consumer)
            time.sleep(5)


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
        words = request.content.split(" ", 2)

        if len(words) > 1 and words[1] == 'full':
            response = ["# Monitor"]

            response.append("## http")

            for key in self.monitor.status['http']:
                response.append("> %s : %s %s" % (self.monitor.status['http'][key]['status'], key, self.servers['http'][key]['url']))

            return "\n".join(response)
        else:
            for key in self.monitor.status['http']:
                if self.monitor.status['http'][key]['status'] == 'ko':
                    return "Some components are not responding, please run `monitor full` for more information"

            return "All components are running"


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
