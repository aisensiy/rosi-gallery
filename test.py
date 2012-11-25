import main
import json
import unittest


class RosiViewTest(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()

    def tearDown(self):
        pass

    def assert_list_data(self, result):
        data = json.loads(result.data)
        assert type(data) is list
        assert len(data) is not 0

    def test_list_api(self):
        result = self.app.get('/list')
        self.assert_list_data(result)

    def test_popular(self):
        result = self.app.get('popular')
        self.assert_list_data(result)


if __name__ == "__main__":
    unittest.main()
