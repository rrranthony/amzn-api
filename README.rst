============================== 
Amazon Product Advertising API
============================== 

This module offers very basic access to `Amazon's Product Advertising API`_.
Currently the only supported functionality is the item lookup in the Movies
search index.

.. _Amazon's Product Advertising API:
   http://docs.aws.amazon.com/AWSECommerceService/latest/GSG/Welcome.html


Usage
=====

Once you've registered as an `Amazon Associate`_, create the file
``~/.amzn-api`` with the following data::

    [credentials]
    aws_access_key_id = <your aws access key id>
    aws_secret_access_key = <your aws secret access key>
    associate_tag = <your associate tag>

Here is a basic item lookup using UPC::

    >>> from amzn.api import API
    >>> api = API()
    >>> result = api.item_lookup(item_id='024543206507', id_type='UPC')
    >>> for key in sorted(result.keys()):
    ...     print('{}: {}'.format(key, result[key]))
    ...
    ASIN: B017S3OP34
    AmazonNewPrice: $10.49
    AmazonProductUrl: http://www.amazon.com/dp/B017S3OP34
    Binding: Blu-ray
    Director: Ridley Scott
    EAN: 0024543206507
    LowestNewPrice: $9.96
    NumberOfDiscs: 1
    ReleaseDate: 2016-01-12
    Title: The Martian [Blu-ray]
    UPC: 024543206507

This module also includes a convenience script, ``amazon_item_lookup``.  To
use the script, this module can be installed using pip::

    pip install git+https://github.com/rrranthony/amzn-api.git

Run ``amazon_item_lookup --help`` to see usage information::

    $ amazon_item_lookup --help
    usage: amazon_item_lookup [-h] [--csv-outfile CSV_OUTFILE]
                              {UPC,EAN,ASIN} item_id [item_id ...]

    Look up items in Amazon's movie library. If a CSV_OUTFILE is given, results
    will be written in CSV format to the file. Otherwise, results will be printed
    to STDOUT.

    positional arguments:
      {UPC,EAN,ASIN}        ID type of the item(s) to look up
      item_id               item ID to look up

    optional arguments:
      -h, --help            show this help message and exit
      --csv-outfile CSV_OUTFILE
                            file to write results to in CSV forma

.. _Amazon Associate:
   http://docs.aws.amazon.com/AWSECommerceService/latest/DG/becomingAssociate.html


Notes
=====

Some parts of this module are based on Sebastian Rahlf's
`python-amazon-product-api`_.

.. _python-amazon-product-api:
   https://bitbucket.org/basti/python-amazon-product-api
