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
        
        for flow in self.container.parameters.get('consumers'):
            if not self.container.has("consumer.%s.flowdock" % flow):
                continue

            consumers[flow] = self.container.get("consumer.%s.flowdock" % flow)

            if not args.debug:
                twistedhttpstream.stream(
                    self.container.get('ioc.extra.twisted.reactor'), 
                    "https://stream.flowdock.com/flows/%s/%s" % (self.container.parameters.get("flowdock.%s.organisation" % flow), flow), 
                    self.container.get("consumer.%s.flowdock" % flow), 
                    username=self.container.parameters.get("flowdock.user.token"),
                    password=""
                )
        
        if args.debug:
            stdio.StandardIO(StdioProtocol(self.container.get('shirka.bot'), consumers, user_id=1))


        self.container.get('ioc.extra.twisted.reactor').run()