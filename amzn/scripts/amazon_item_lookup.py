import argparse
import sys

from ..api import API
from ..common import VALID_ID_TYPES
from ..utils import write_results_to_csv


def main():
    description = ("Look up items in Amazon's movie library.  If a CSV_OUTFILE is given, results will be written in "
                   "CSV format to the file.  Otherwise, results will be printed to STDOUT.")
    argparser = argparse.ArgumentParser(description=description)
    argparser.add_argument('id_type', choices=VALID_ID_TYPES,
                           help='ID type of the item(s) to look up')
    argparser.add_argument('item_id', nargs='+', help='item ID to look up')
    argparser.add_argument('--csv-outfile', help='file to write results to in CSV format')
    args = argparser.parse_args()
    api = API()
    results = []
    for item_id in args.item_id:
        # TODO(rrranthony): add progress, e.g., looking up item X of Y...
        result = api.lookup_item(item_id=item_id, id_type=args.id_type)
        results.append(result)
        if args.csv_outfile is None:
            for field in result:
                print('{}: {}'.format(field, result[field]))
            print('')
    if args.csv_outfile:
        write_results_to_csv(results, API.RESULT_FIELDNAMES, args.csv_outfile)


if __name__ == '__main__':
    main()
