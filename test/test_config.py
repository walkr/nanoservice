import json
import unittest

from nanoservice import config


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.addr = 'ipc:///tmp/test-service.sock'
        self.expected = {
            "db.name": "test",
            "service.endpoint": self.addr
        }

    def tearDown(self):
        pass

    def test_config_load(self):
        C = config.load("test/testdata/service.json", clients=False)
        self.assertTrue(C.keys(), self.expected.keys())
        self.assertTrue(C.values(), self.expected.values())

    def test_config_load_with_content(self):
        filec = json.dumps(self.expected)
        C = config.load(filecontent=filec, clients=False)
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
