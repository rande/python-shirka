from __future__ import absolute_import

import paramiko, unittest, os

class Paramiko(object):
    def build_client_args(self, config):
        args = {}

        defaults = [
            ('port', 22),  ('username', None),  ('password', None), 
            ('pkey', None), ('key_filename', None), ('timeout', None), 
            ('allow_agent', True), ('look_for_keys', True), 
            ('compress', False)
        ]

        for default in defaults:
            key, value = default
            args[key] = value if key not in config else config[key]

            if key == 'pkey' and args[key] and not isinstance(args[key], paramiko.PKey):
                if os.path.exists(args[key]):
                    args[key] = paramiko.RSAKey(filename=args[key])
                else:
                    args[key] = paramiko.RSAKey(data=args[key])

        return args

    def get_client(self, host, config):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, **self.build_client_args(config))

        return client

class ParamikoTest(unittest.TestCase):
    def setUp(self):
        self.paramiko = Paramiko()

    def test_build_client_args(self):
        args = self.paramiko.build_client_args({'port': 23, 'look_for_keys': False})

        expected = {
            'port': 23,
            'username': None,
            'password': None,
            'pkey': None,
            'key_filename': None,
            'timeout': None,
            'allow_agent': True,
            'look_for_keys': False,
            'compress': False
        }

        self.assertEquals(args, expected)