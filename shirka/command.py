from ioc.extra.command import Command
from shirka.consumers.stdio import StdioProtocol
from twisted.internet import stdio
import twistedhttpstream

class StartCommand(Command):
    def __init__(self, container):
        self.container = container

    def initialize(self, parser):
        parser.description = 'Start shirka bot'

    def execute(self, args, output):
        output.write("Starting shirka ...\n")

        consumers = {}
        reactor = self.container.get('ioc.extra.twisted.reactor')

        for flow in self.container.parameters.get('consumers'):
            output.write(" > flow %s" % flow)
            if not self.container.has("shirka.consumer.flowdock.%s" % flow):
                continue

            consumers[flow] = self.container.get("shirka.consumer.flowdock.%s" % flow)

            if not args.debug:
                url = "https://stream.flowdock.com/flows/%s/%s" % (self.container.parameters.get("shirka.flowdock.%s.organisation" % flow), flow)
                consumer = self.container.get("shirka.consumer.flowdock.%s" % flow)
                token = self.container.parameters.get("shirka.flowdock.user.token")

                twistedhttpstream.stream(reactor, url, consumers[flow], username=token, password="")
        
        if args.debug:
            stdio.StandardIO(StdioProtocol(self.container.get('shirka.bot'), consumers, user_id=1))

        reactor.run()