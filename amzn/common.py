import os


REQUIRED_CONFIG_KEYS = [
    'aws_access_key_id',
    'aws_secret_access_key',
    'associate_tag',
]

CONFIG_FILE = '~/.amzn-api'

VALID_ID_TYPES = [
    'UPC',
    'EAN',
    'ASIN',
]

_package_dir = os.path.dirname(os.path.abspath(__file__))
ETC_DIR = os.path.join(_package_dir, 'etc')
CACHE_DIR = os.path.join(ETC_DIR, 'cache')
