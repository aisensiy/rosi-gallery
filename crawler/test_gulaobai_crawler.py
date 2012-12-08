import unittest
import re
from gulaobai_crawler import get_img_urls

class GulaobaiTestCase(unittest.TestCase):
    def test_get_img_urls(self):
        results = get_img_urls('http://gulaobai.diandian.com/post/2012-11-19/40042571009')
        self.assertTrue(re.match('^http.+', results[0]))

if __name__ == '__main__':
    unittest.main()
