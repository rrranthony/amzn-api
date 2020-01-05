import json
import os

from .common import CACHE_DIR


class MissingItemLookupResponse(Exception):
    pass


class CacheDoesNotExist(Exception):
    pass


class ItemLookup:
    """Class summary.

    More info
    """

    def __init__(self, item_lookup_parameters, item_lookup_response_text=None):
        self._item_lookup_parameters = item_lookup_parameters
        self._item_lookup_response_text = item_lookup_response_text
        cache_basename = '{id_type}_{item_id}.json'.format(
            id_type=self._item_lookup_parameters['IdType'],
            item_id=self._item_lookup_parameters['ItemId'])
        self._cache_filename = os.path.join(CACHE_DIR, cache_basename)

    def cache_exists(self):
        return os.path.isfile(self._cache_filename)

    def load_from_cache(self):
        if self.cache_exists():
            with open(self._cache_filename, 'r') as f:
                return json.load(f)
        raise CacheDoesNotExist

    def set_item_lookup_response_text(self, item_lookup_response_text):
        self._item_lookup_response_text = item_lookup_response_text

    def cache(self, overwrite=True):
        if self._item_lookup_response_text is None:
            raise MissingItemLookupResponse('Item lookup response is not set, unable to cache')
        cache_dict = {
            'item_lookup_parameters': self._item_lookup_parameters,
            'item_lookup_response_text': self._item_lookup_response_text
        }
        with open(self._cache_filename, 'w') as f:
            json.dump(cache_dict, f, indent=4 * ' ')
