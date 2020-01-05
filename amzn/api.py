import copy
from datetime import datetime
import time

import requests
import xmltodict

from .common import REQUIRED_CONFIG_KEYS
from .ItemLookup import ItemLookup
from .utils import load_config, now_utc_str
from .utils import build_canonical_query_string, build_string_to_sign, create_signature, \
        build_request_url, get_amazon_product_url, parse_item_attributes, parse_item_price


class API:
    REQUESTS_PER_SECOND = 0.5
    ENDPOINT = 'webservices.amazon.com'
    REQUEST_URI = '/onca/xml'  # URI is always the same for Amazon Product Advertising API requests
    ITEM_LOOKUP_PARAMS = {
        'Service': 'AWSECommerceService',
        'Operation': 'ItemLookup',
        'SearchIndex': 'Movies',
        'ResponseGroup': 'ItemAttributes,Offers',
    }
    RESULT_FIELDNAMES = [
        'ASIN',
        'AmazonNewPrice',
        'AmazonNewPriceCurrencyCode',
        'AmazonProductUrl',
        'Binding',
        'Director',
        'EAN',
        'Format',
        'LookupDateTimeUtc',
        'LookupIdType',
        'LookupItemId',
        'LowestCollectiblePrice',
        'LowestCollectiblePriceCurrencyCode',
        'LowestNewPrice',
        'LowestNewPriceCurrencyCode',
        'LowestUsedPrice',
        'LowestUsedPriceCurrencyCode',
        'NumberOfDiscs',
        'RegionCode',
        'ReleaseDate',
        'RunningTime',
        'Studio',
        'Title',
        'UPC'
    ]

    def __init__(self, cache_lookups=True):
        self._cache_lookups = cache_lookups
        config = load_config()
        for key in REQUIRED_CONFIG_KEYS:
            setattr(self, key, config[key])
        self._last_request_time = datetime(1970, 1, 1)
        self._minimum_seconds_between_requests = 1.0 / type(self).REQUESTS_PER_SECOND

    def _throttle(self):
        since = datetime.now() - self._last_request_time
        seconds_since_last_request = since.seconds + since.microseconds / 1000000.0
        if seconds_since_last_request < self._minimum_seconds_between_requests:
            wait = self._minimum_seconds_between_requests - seconds_since_last_request
            time.sleep(wait)

    def _update_last_request_time(self):
        self._last_request_time = datetime.now()

    def _build_item_lookup_parameters(self, item_id, id_type):
        params = copy.deepcopy(type(self).ITEM_LOOKUP_PARAMS)
        if id_type == 'ASIN':
            # SearchIndex cannot be present when id_type is ASIN
            del params['SearchIndex']
        params['AWSAccessKeyId'] = self.aws_access_key_id
        params['AssociateTag'] = self.associate_tag
        params['ItemId'] = item_id
        params['IdType'] = id_type  # UPC, EAN, ASIN
        params['Timestamp'] = now_utc_str()
        return params

    def _build_item_lookup_request_url(self, item_lookup_parameters):
        # Info on REST signature:
        # https://docs.aws.amazon.com/AWSECommerceService/latest/DG/rest-signature.html
        canonical_query_string = build_canonical_query_string(item_lookup_parameters)
        string_to_sign = build_string_to_sign(
            type(self).ENDPOINT,
            type(self).REQUEST_URI,
            canonical_query_string
        )
        signature = create_signature(self.aws_secret_access_key, string_to_sign)
        request_url = build_request_url(
            type(self).ENDPOINT,
            type(self).REQUEST_URI,
            canonical_query_string,
            signature
        )
        return request_url

    def _parse_item_lookup_response_text(self, item_lookup_response_text):
        result = {}
        response_dict = xmltodict.parse(item_lookup_response_text)
        item_lookup_response = response_dict['ItemLookupResponse']
        items = item_lookup_response['Items']
        item = items['Item']
        result['ASIN'] = item.get('ASIN')
        result['AmazonProductUrl'] = None
        if result['ASIN']:
            result['AmazonProductUrl'] = get_amazon_product_url(result['ASIN'])
        item_attributes = parse_item_attributes(item)
        result.update(item_attributes)
        item_price = parse_item_price(item)
        result.update(item_price)
        return result

    def lookup_item(self, item_id, id_type):
        from_cache = False
        item_lookup_parameters = self._build_item_lookup_parameters(item_id, id_type)
        item_lookup = ItemLookup(item_lookup_parameters)
        if item_lookup.cache_exists():
            cached_item_lookup = item_lookup.load_from_cache()
            response_text = cached_item_lookup['item_lookup_response_text']
            from_cache = True
        else:
            request_url = self._build_item_lookup_request_url(item_lookup_parameters)
            self._throttle()
            response = requests.get(request_url)
            response_text = response.text
            if self._cache_lookups:
                item_lookup.set_item_lookup_response_text(response_text)
                item_lookup.cache()
            self._update_last_request_time()
        result = self._parse_item_lookup_response_text(response_text)
        if from_cache:
            result.update({'LookupDateTimeUtc': cached_item_lookup['item_lookup_parameters']['Timestamp']})
        else:
            result.update({'LookupDateTimeUtc': now_utc_str()})
        result.update({'LookupIdType': id_type})
        result.update({'LookupItemId': item_id})
        return result
