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
        C = config.load("nanoservice/test/testdata/service.json", clients=False)
        self.assertTrue(C.keys(), self.expected.keys())
        self.assertTrue(C.values(), self.expected.values())

    def test_config_load_with_content(self):
        filec = json.dumps(self.expected)
        C = config.load(filecontent=filec, clients=False)
        self.assertTrue(C.keys(), self.expected.keys())
        self.assertTrue(C.values(), self.expected.values())


if __name__ == '__main__':
    unittest.main()
