REQUIRED_CONFIG_KEYS = [
    'aws_access_key_id',
    'aws_secret_access_key',
    'associate_tag',
]

CONFIG_FILE = '~/.amzn-api'

ENDPOINT = 'webservices.amazon.com'

# URI is always the same for Amazon Product Advertising API requests
REQUEST_URI = '/onca/xml'

ITEM_LOOKUP_PARAMS = {
    'Service': 'AWSECommerceService',
    'Operation': 'ItemLookup',
    'SearchIndex': 'Movies',
    'ResponseGroup': 'ItemAttributes,Offers',
}

VALID_ID_TYPES = [
    'UPC',
    'EAN',
    'ASIN',
]
