import argparse
import sys

from ..api import API
from ..common import VALID_ID_TYPES


def main():
    description = "Look up items in Amazon's movie library."
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('id_type', choices=VALID_ID_TYPES,
                           help='ID type of the item(s) to look up')
    argparser.add_argument('item_id', nargs='+', help='item ID to look up')
    args = argparser.parse_args()
    api = API()
    result = api.item_lookup(item_id=args.item_id, id_type=args.id_type)
    for key in sorted(result.keys()):
        print('{}: {}'.format(key, result[key]))


if __name__ == '__main__':
    main()
