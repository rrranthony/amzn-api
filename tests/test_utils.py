import unittest

from amzn.utils import build_string_to_sign
from amzn.utils import get_amazon_product_url


class TestUtils(unittest.TestCase):

    def test_build_string_to_sign(self):
        string_to_sign = build_string_to_sign('endpoint', 'request_uri', 'canonical_query_string')
        expected_string_to_sign = 'GET\nendpoint\nrequest_uri\ncanonical_query_string'
        self.assertEqual(string_to_sign, expected_string_to_sign)

    def test_get_amazon_product_url(self):
        url = get_amazon_product_url('ABCDE01234')
        expected_url = 'http://www.amazon.com/dp/ABCDE01234'
        self.assertEqual(url, expected_url)


if __name__ == '__main__':
    unittest.main()
