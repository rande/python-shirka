# vim: set fileencoding=utf-8 :

from twisted.protocols import basic
from shirka.consumers import Request, User, StreamAssistant, Consumer
from shirka.responders import Responder, Response, StreamResponse

class StdioProtocol(basic.LineReceiver, Consumer):
    """
    This consumer must be used for debbuging only
    """
    delimiter = "\n"

    def __init__(self, bot, consumers, user_id=0):
        self.bot = bot
        self.consumers = consumers
        self.user_id = user_id
        self.stream_assistant = StreamAssistant(self)
        self.consumer = False

    def create_request(self, text):
        return Request(text, User(None, None, int(self.user_id)), 'message', 'cli')

    def prompt(self):
        self.transport.write(("%s (%s)$ " % (self.bot.name, self.consumer)).encode("utf-8"))

    def connectionMade(self):
        self.sendLine("Debug console. Type 'help' for help.")

        for name, consumer in self.consumers.iteritems():
            for id, responder in consumer.responders:
                self.handle_response(
                    responder.on_start(consumer), 
                    Request('on_start', User(None, None, self.user_id), 'init', 'cli')
                )

        if len(self.consumers) == 1:
            self.consumer = self.consumers.keys()[0]

        self.prompt()

    def lineReceived(self, line):
        try:
            self._lineReceived(line)
        except Exception, e:
            import traceback
            traceback.print_exc()

        self.prompt()

    def _lineReceived(self, line):
        """
        channel command
        """
        if not line: return

        commandParts = line.split()
        command     = commandParts[0].lower()

        if command == "h":
            self.do_help()
            return

        if command == "with" and not self.consumer:
            if len(commandParts) != 2:
                self.sendLine("ERROR: with requires the consumer name")
                return

            if commandParts[1] not in self.consumers.keys():
                self.sendLine("ERROR: no consumer found: %s" % (commandParts[1]))
                return
            
            self.consumer = commandParts[1]

            return

        if command == "end" and self.consumer:
            self.consumer = False
            return

        request = self.create_request(line)
        responses = self.consumers[self.consumer].handle_message(request)

        for response in responses:
            self.handle_response(response, request)

    def do_help(self):
        message = "Allows to execute command on the cli instead of the gui \n"
        message += "This can be usefull to debug a command without using the official channel\n\n"
        message += "Usage: with CHANNEL\n"
        message += "Usage: COMMAND\n"
        message += "Usage: end\n"

        self.sendLine(message)

    def handle_response(self, response, request):
        if isinstance(response, StreamResponse):
            response.handle(request, self)
            # self.stream_assistant.add(response, request)
        else:
            self.post(response, request)

    def post(self, response, request):

        response = self.normalize(response, request)

        if response in [False, None]:
            return

        if not response.content:
            return

        for line in response.content.split("\n"):
            self.sendLine((u" » %s" % line).encode("utf-8"))