# vim: set fileencoding=utf-8 :
from shirka.responders import Responder, StreamResponse
from shirka.consumers import BaseTestCase
import paramiko, os

class RemoteStreamResponse(StreamResponse):
    def __init__(self, name, server, cmd, paramiko):
        self._server = server
        self._name = name
        self._cmd = cmd
        self._paramiko = paramiko

    def handle(self, request, consumer):
        consumer.post("Order received: %s$ %s" % (self._name, self._cmd), request)

        try:
            client = self._paramiko.get_client(self._server['host'], self._server)
        except Exception, e:
            consumer.post("Error while getting paramiko client: %s" % e, request)
            
            raise e

        try:
            stdin, stdout, stderr = client.exec_command(self._cmd)

            message = "> " + "> ".join(stdout.readlines())

            consumer.post(message, request)

        except paramiko.SSHException, e:
            consumer.post("An error occurs while executing the command: %s$ %s " % (self._name, self._cmd), request)

            raise e
        finally:
            client.close()


class RemoteResponder(Responder):
    def __init__(self, servers, users, paramiko):
        self.servers = servers
        self.users = users
        self.paramiko = paramiko

    def name(self):
        return "ssh"

    def generate(self, request):
        """
        usage: ssh server command
        run a command on an remote server
        """
        if request.user.id not in self.users:
            return "You fool, you are not my master!!"

        words = request.content.split(" ", 2)

        if len(words) < 2:
            return "Invalid command"

        if words[1] not in self.servers:
            return "Sorry, there is no such server available"


        return RemoteStreamResponse(words[1], self.servers[words[1]].copy(), words[2], self.paramiko)
        