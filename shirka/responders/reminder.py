# vim: set fileencoding=utf-8 :

from shirka.responders import Responder, StreamResponse
import requests, json, re, time, threading
from shirka.consumers import BaseTestCase

class ReminderStreamResponse(StreamResponse):
    def handle(self, request, consumer):
        consumer.post("Roger that!! (reminder set)", request)

        def remind():
            consumer.post("Reminder: %s" % self.content, request)

        t = threading.Timer(self.end - time.time(), remind)
        t.run()

class ReminderResponder(Responder):

    def __init__(self):
        self.pattern = re.compile("^(?P<CMD>reminder|in)"
                                  "\\s(?P<TIME>[0-9]+)"
                                  "\\s?(?P<UNIT>s|second|seconds|mn|minute|minutes|h|hour|hours|d|day|days|m|month|months|y|year|years)"
                                  "\\s(?P<MSG>.*)$")
        self.unitMapping = {
            'second': {'seconds': float(1),                      'abbr': 's',  'plural': 'seconds'},
            'minute': {'seconds': float(60),                     'abbr': 'mn', 'plural': 'minutes'},
            'hour':   {'seconds': float(60 * 60),                'abbr': 'h',  'plural': 'hours'},
            'day':    {'seconds': float(60 * 60 * 24),           'abbr': 'd',  'plural': 'days'},
            'month':  {'seconds': float(60 * 60 * 24 * 30),      'abbr': 'm',  'plural': 'months'},
            'year':   {'seconds': float(60 * 60 * 24 * 30 * 12), 'abbr': 'y',  'plural': 'years'}
        }
        super(ReminderResponder, self).__init__()

    def name(self):
        return 'reminder'

    def support(self, request):
        return True

    def generate(self, request):
        """
        usage: reminder time message
        alt usage: in time message
        store a reminder, time must be integer + unit : 15s or 15m. 
        valid unit: s (second), m (minute) and h (hour)
        """

        result = self.pattern.match(request.content)

        if result is None:
            return False

        time = result.groupdict()['TIME']
        unit = result.groupdict()['UNIT']
        normalized_unit = self.normalize_unit(unit)
        message = result.groupdict()['MSG']
        message += " (%s %s ago)" % (time, self.pluralize_unit(time, normalized_unit))

        end = self.get_time(time, normalized_unit)

        response = ReminderStreamResponse(message)
        response.end = end

        return response

    def normalize_unit(self, unit):
        for key in self.unitMapping:
            if unit in (key, self.unitMapping[key]['abbr'], self.unitMapping[key]['plural']):
                return key

    def pluralize_unit(self, amount, unit):
        if int(amount) > 1:
            return self.unitMapping[unit]['plural']

        return unit

    def get_time(self, amount, unit):

        amount = float(amount)
        base = time.time()

        return base + amount * self.unitMapping[unit]['seconds']


class TestReminderResponder(BaseTestCase):
    def setUp(self):
        self.responder = ReminderResponder()

    def test_support(self):
        self.assertTrue(self.responder.support(self.create_request("reminder")))
        self.assertTrue(self.responder.support(self.create_request("fuu")))

    def test_no_match(self):
        self.assertFalse(self.generate("reminder"))
        self.assertFalse(self.generate("reminder 1s"))
        self.assertFalse(self.generate("in"))
        self.assertFalse(self.generate("in 4mn"))

    def test_invalid_time(self):
        self.assertFalse(self.generate("reminder 15j see raph about webservices"))

    def test_normalize_unit(self):
        self.assertEquals('second', self.responder.normalize_unit('s'))
        self.assertEquals('second', self.responder.normalize_unit('second'))
        self.assertEquals('second', self.responder.normalize_unit('seconds'))
        self.assertEquals('minute', self.responder.normalize_unit('mn'))
        self.assertEquals('minute', self.responder.normalize_unit('minute'))
        self.assertEquals('minute', self.responder.normalize_unit('minutes'))
        self.assertEquals('hour', self.responder.normalize_unit('h'))
        self.assertEquals('hour', self.responder.normalize_unit('hour'))
        self.assertEquals('hour', self.responder.normalize_unit('hours'))
        self.assertEquals('day', self.responder.normalize_unit('d'))
        self.assertEquals('day', self.responder.normalize_unit('day'))
        self.assertEquals('day', self.responder.normalize_unit('days'))
        self.assertEquals('month', self.responder.normalize_unit('m'))
        self.assertEquals('month', self.responder.normalize_unit('month'))
        self.assertEquals('month', self.responder.normalize_unit('months'))
        self.assertEquals('year', self.responder.normalize_unit('y'))
        self.assertEquals('year', self.responder.normalize_unit('year'))
        self.assertEquals('year', self.responder.normalize_unit('years'))

    def test_pluralize_unit(self):
        self.assertEquals('second', self.responder.pluralize_unit(1, 'second'))
        self.assertEquals('seconds', self.responder.pluralize_unit(2, 'second'))
        self.assertEquals('minute', self.responder.pluralize_unit(1, 'minute'))
        self.assertEquals('minutes', self.responder.pluralize_unit(2, 'minute'))
        self.assertEquals('hour', self.responder.pluralize_unit(1, 'hour'))
        self.assertEquals('hours', self.responder.pluralize_unit(2, 'hour'))
        self.assertEquals('day', self.responder.pluralize_unit(1, 'day'))
        self.assertEquals('days', self.responder.pluralize_unit(2, 'day'))
        self.assertEquals('month', self.responder.pluralize_unit(1, 'month'))
        self.assertEquals('months', self.responder.pluralize_unit(2, 'month'))
        self.assertEquals('year', self.responder.pluralize_unit(1, 'year'))
        self.assertEquals('years', self.responder.pluralize_unit(2, 'year'))

    def test_valid(self):
        response = self.generate("reminder 0s see raph about webservices")
        self.assertIsInstance(response, ReminderStreamResponse)
        self.assertIsNotNone(response.end)
        response = self.generate("reminder 0 s see raph about webservices")
        self.assertIsInstance(response, ReminderStreamResponse)
        self.assertIsNotNone(response.end)
        response = self.generate("reminder 0second see raph about webservices")
        self.assertIsInstance(response, ReminderStreamResponse)
        self.assertIsNotNone(response.end)
        response = self.generate("reminder 0 second see raph about webservices")
        self.assertIsInstance(response, ReminderStreamResponse)
        self.assertIsNotNone(response.end)
        response = self.generate("reminder 0seconds see raph about webservices")
        self.assertIsInstance(response, ReminderStreamResponse)
        self.assertIsNotNone(response.end)
        response = self.generate("reminder 0 seconds see raph about webservices")
        self.assertIsInstance(response, ReminderStreamResponse)
        self.assertIsNotNone(response.end)

    def test_on_start(self):
        self.assertFalse(self.responder.on_start(False))

