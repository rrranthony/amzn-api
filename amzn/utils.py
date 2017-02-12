import configparser
import csv
import os
import urllib
import hmac
import hashlib
import base64
from time import strftime, gmtime

from .common import REQUIRED_CONFIG_KEYS, CONFIG_FILE


def load_config():
    config = configparser.ConfigParser()
    config.read(os.path.expanduser(CONFIG_FILE))
    config_dict = dict(
        (key, value)
        for key, value in config.items('credentials')
        if key in REQUIRED_CONFIG_KEYS
    )
    return config_dict


def now_utc_str():
    return strftime('%Y-%m-%dT%H:%M:%SZ', gmtime())


def build_canonical_query_string(params):
    # Take a dict of params and return the canonical query string: sorted
    # param/value pairs, urlencoded
    sorted_param_value_pairs = [(key, params[key]) for key in sorted(params.keys())]
    canonical_query_string = urllib.parse.urlencode(sorted_param_value_pairs)
    # Use quote_via=urllib.parse.quote() because urlencode defaults to
    # quote_via=urllib.parse.quote_plus().  quote_plus() quotes spaces as '+',
    # but the Amazon API expects spaces encoded as '%20'.  quote() uses the
    # '%20' quoting for spaces.
    canonical_query_string = urllib.parse.urlencode(sorted_param_value_pairs,
                                                    quote_via=urllib.parse.quote)
    return canonical_query_string


def build_string_to_sign(endpoint, request_uri, canonical_query_string):
    string_to_sign = 'GET\n{endpoint}\n{request_uri}\n{canonical_query_string}'.format(
            endpoint=endpoint,
            request_uri=request_uri,
            canonical_query_string=canonical_query_string)
    return string_to_sign


def create_signature(aws_secret_access_key, string_to_sign):
    # hmac sha256 signature creation reference: http://stackoverflow.com/a/1307439
    digest = hmac.new(key=bytes(aws_secret_access_key, 'utf-8'),
                      msg=bytes(string_to_sign, 'utf-8'),
                      digestmod=hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode('utf-8')
    return signature


def build_request_url(endpoint, request_uri, canonical_query_string, signature):
    request_url = ('http://{endpoint}{request_uri}?{canonical_query_string}&'
                   'Signature={signature}').format(
                           endpoint=endpoint,
                           request_uri=request_uri,
                           canonical_query_string=canonical_query_string,
                           signature=urllib.parse.quote(signature))
    return request_url


def get_amazon_product_url(asin):
    return 'http://www.amazon.com/dp/{}'.format(asin)


def _parse_attribute_format(format_):
    if isinstance(format_, list):
        if 'NTSC' in format_:
            format_ = 'NTSC'
        elif 'PAL' in format_:
            format_ = 'PAL'
        else:
            # Only values like 'Color', 'Widescreen', etc. are given.  Since we just want NTSC or PAL, null this out.
            format_ = None
    return format_


def parse_item_attributes(item):
    result = {}
    item_attributes = item.get('ItemAttributes')
    # If an attribute appears multiple times, e.g.,
    #
    #   <Actor>actor1</Actor>
    #   <Actor>actor2</Actor>
    #
    # the value using the key will be a list instead of a string, e.g., ['actor1', 'actor2'], instead of just 'actor1'.
    if item_attributes:
        result['Binding'] = item_attributes.get('Binding')
        result['Director'] = item_attributes.get('Director')
        result['EAN'] = item_attributes.get('EAN')
        result['Format'] = _parse_attribute_format(item_attributes.get('Format'))
        result['NumberOfDiscs'] = item_attributes.get('NumberOfDiscs')
        result['RegionCode'] = item_attributes.get('RegionCode')
        result['ReleaseDate'] = item_attributes.get('ReleaseDate')
        result['Studio'] = item_attributes.get('Studio')
        result['Title'] = item_attributes.get('Title')
        result['UPC'] = item_attributes.get('UPC')
    return result


def parse_item_price(item):
    result = {}
    # Non-Amazon
    offer_summary = item.get('OfferSummary')
    if offer_summary:
        lowest_new_price = offer_summary.get('LowestNewPrice')
        if lowest_new_price:
            result['LowestNewPrice'] = lowest_new_price.get('FormattedPrice')
            result['LowestNewPriceCurrencyCode'] = lowest_new_price.get('CurrencyCode')
        lowest_used_price = offer_summary.get('LowestUsedPrice')
        if lowest_used_price:
            result['LowestUsedPrice'] = lowest_used_price.get('FormattedPrice')
            result['LowestUsedPriceCurrencyCode'] = lowest_used_price.get('CurrencyCode')
        lowest_collectible_price = offer_summary.get('LowestCollectiblePrice')
        if lowest_collectible_price:
            result['LowestCollectiblePrice'] = lowest_collectible_price.get('FormattedPrice')
            result['LowestCollectiblePriceCurrencyCode'] = lowest_collectible_price.get('CurrencyCode')
    # Amazon new.  Use the highest new price.
    offers = item.get('Offers')
    if offers:
        total_offers = int(offers['TotalOffers'])
        if total_offers > 0:
            best_offer_amount = 0
            offer_list = offers['Offer']
            if total_offers == 1:
                offer_list = [offer_list]
            for offer in offer_list:
                condition = offer['OfferAttributes']['Condition']
                if condition == 'New':
                    price = offer['OfferListing']['Price']
                    offer_amount = int(price['Amount'])
                    if offer_amount > best_offer_amount:
                        best_offer_amount = offer_amount
                        result['AmazonNewPrice'] = price.get('FormattedPrice')
                        result['AmazonNewPriceCurrencyCode'] = price.get('CurrencyCode')
    return result


def prepare_result_for_csv_output(result, output_fieldnames):
    # TODO(rrranthony): format list values to something else?
    if result is None:
        result = {}
    for fieldname in output_fieldnames:
        if result.get(fieldname) is None:
            result[fieldname] = 'NULL'
    return result


def write_results_to_csv(results, csv_fieldnames, csv_filename):
    prepared_results = []
    for result in results:
        prepared_results.append(prepare_result_for_csv_output(result, csv_fieldnames))
    with open(csv_filename, 'w') as csv_outfile:
        writer = csv.DictWriter(csv_outfile, fieldnames=csv_fieldnames)
        writer.writeheader()
        for prepared_result in prepared_results:
            writer.writerow(prepared_result)
