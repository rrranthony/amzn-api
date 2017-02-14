from amzn.utils import build_string_to_sign
from amzn.utils import get_amazon_product_url


def test_build_string_to_sign():
    string_to_sign = build_string_to_sign('endpoint', 'request_uri', 'canonical_query_string')
    expected_string_to_sign = 'GET\nendpoint\nrequest_uri\ncanonical_query_string'
    assert string_to_sign == expected_string_to_sign


def test_get_amazon_product_url():
    url = get_amazon_product_url('ABCDE01234')
    expected_url = 'http://www.amazon.com/dp/ABCDE01234'
    assert url == expected_url
