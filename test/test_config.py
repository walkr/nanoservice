import json
import unittest

from nanoservice import *
from nanoservice import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.addr = 'ipc:///whatever'
        self.expected = {
            'db.name': 'test',
            'rq.requester': 'ipc:///whatever',
            'rs.responder': 'ipc:///whatever',
            'pb.publisher': 'ipc:///whatever',
            'sb.subscriber': 'ipc:///whatever',
        }

    def tearDown(self):
        pass

    def test_config_load(self):
        C = config.load("test/testdata/configuration.json")
        self.assertTrue(C.keys(), self.expected.keys())
        self.assertTrue(C.values(), self.expected.values())

    def test_config_load_with_content(self):
        filec = json.dumps(self.expected)
        C = config.load(filecontent=filec)
        self.assertTrue(C.keys(), self.expected.keys())
        self.assertTrue(C.values(), self.expected.values())

    def test_dot_dict_get_and_set(self):
        d = config.DotDict()
        d['name'] = 'John Doe'
        self.assertEqual(getattr(d, 'name'), 'John Doe')
        d.age = '20'
        self.assertEqual(getattr(d, 'age'), '20')


if __name__ == '__main__':
    unittest.main()
