from unittest.mock import Mock, patch

from amzn.utils import now_utc_str, build_canonical_query_string, build_string_to_sign, create_signature, \
    build_request_url, get_amazon_product_url, _parse_attribute_format, parse_item_attributes


@patch('amzn.utils.gmtime')
@patch('amzn.utils.strftime')
def test_now_utc_str(mock_strftime, mock_gmtime):
    now_utc_str()
    mock_strftime.assert_called_once_with('%Y-%m-%dT%H:%M:%SZ', mock_gmtime())


def test_build_canonical_query_string():
    params = {'foo': 'bar', 'jane': 'doe', 'name': 'john doe'}
    expected_query_string = 'foo=bar&jane=doe&name=john%20doe'
    assert build_canonical_query_string(params) == expected_query_string


def test_build_string_to_sign():
    string_to_sign = build_string_to_sign('endpoint', 'request_uri', 'canonical_query_string')
    expected_string_to_sign = 'GET\nendpoint\nrequest_uri\ncanonical_query_string'
    assert string_to_sign == expected_string_to_sign


def test_create_signature():
    aws_secret_access_key = 'foo'
    string_to_sign = 'bar'
    expected_signature = '+TILrwJJFp5zhQzWFW3tAQbiu2rYyrAbe7vr5tEGUxc='
    assert create_signature(aws_secret_access_key, string_to_sign) == expected_signature


def test_build_request_url():
    endpoint = 'foo'
    request_uri = 'bar'
    canonical_query_string = 'get'
    signature = 'john'
    expected_url = 'http://foobar?get&Signature=john'
    assert build_request_url(endpoint, request_uri, canonical_query_string, signature) == expected_url


def test_get_amazon_product_url():
    url = get_amazon_product_url('ABCDE01234')
    expected_url = 'http://www.amazon.com/dp/ABCDE01234'
    assert url == expected_url


def test_parse_attribute_format():
    formats = [
        ['NTSC', 'Color'],
        'PAL',
        ['Widescreen', 'PAL'],
        ['Color', 'Widescreen']
    ]
    expected_formats = [
        'NTSC',
        'PAL',
        'PAL',
        None
    ]
    for i, format_ in enumerate(formats):
        assert _parse_attribute_format(format_) == expected_formats[i]


def test_parse_item_attributes():
    item = {}
    expected_result = {}
    assert parse_item_attributes(item) == expected_result
    item = {
        'ItemAttributes': {
            'ASIN': 'B00',
            'Actor': 'Jeff Bridges',
            'Binding': 'DVD',
            'EAN': 'ABC123',
            'Format': 'NTSC',
            'NumberOfDiscs': '2',
            'RegionCode': '1',
            'ReleaseDate': '2017-02-13',
            'Title': 'The Big Lebowski',
            'UPC': '42'
        }
    }
    expected_result = {
        'Binding': 'DVD',
        'Director': None,
        'EAN': 'ABC123',
        'Format': 'NTSC',
        'NumberOfDiscs': '2',
        'RegionCode': '1',
        'ReleaseDate': '2017-02-13',
        'Studio': None,
        'Title': 'The Big Lebowski',
        'UPC': '42'
    }
    assert parse_item_attributes(item) == expected_result
