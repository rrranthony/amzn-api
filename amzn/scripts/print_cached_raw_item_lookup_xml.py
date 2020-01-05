import argparse
import json
import pprint
from xml.dom import minidom


def main():
    description = ('Print raw item lookup XML from CACHE_FILENAME')
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('cache_filename', help='cache file from which to get raw item lookup XML from')
    args = argparser.parse_args()
    with open(args.cache_filename, 'r') as f:
        item_lookup = json.load(f)
        xml_str = item_lookup['item_lookup_response_text']
        print(minidom.parseString(xml_str).toprettyxml(indent=4 * ' '))


if __name__ == '__main__':
    main()
