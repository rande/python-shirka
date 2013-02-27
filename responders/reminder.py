from responders import StreamResponder
import requests, json, unittest, re, time, threading

class ReminderResponder(StreamResponder):

    def __init__(self):
        
        self.pattern = re.compile("")
        super(ReminderResponder, self).__init__()

    def support(self, message):
        return message[0:8] == 'reminder'

    def generate(self, message):
        try:
            cmd, format, message = message.split(" ", 2)
        except Exception, e:
            return False
        
        end = self.get_time(format)

        if not end:
            return False

        self.push("Roger that!! (reminder set)")

        def remind(responder, message):
            responder.push(message)
            responder.stop()

        t = threading.Timer(end - time.time(), remind, [self, message])
        t.run()

        return True

    def get_time(self, number):
        number, format = re.match("([0-9]*)(.*)", number).groups()

        number = float(number)

        base = time.time()

        if format == 's':
            return base + number

        if format == 'm':
            return base + number * 60

        if format == 'h':
            return base + number * 3600

        return False

class TestReminderResponder(unittest.TestCase):
    def setUp(self):
        self.responder = ReminderResponder()

    def test_support(self):
        self.assertTrue(self.responder.support("reminder"))
        self.assertFalse(self.responder.support("fuu"))

    def test_invalid_count(self):
        self.assertFalse(self.responder.generate("reminder"))

    def test_invalid_time(self):
        self.assertFalse(self.responder.generate("reminder 15j see raph about webservices"))

    def test_valid(self):
        self.assertFalse(self.responder.is_completed)
        self.assertTrue(self.responder.generate("reminder 0s see raph about webservices"))
        
        time.sleep(1)

        self.assertEquals(['Roger that!! (reminder set)', 'see raph about webservices'], self.responder.messages)
        self.assertTrue(self.responder.is_completed)
