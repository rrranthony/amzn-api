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
    aws_access_key_id: <your aws access key id>
    aws_secret_access_key: <your aws secret access key>
    associate_tag: <your associate tag>

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

.. _Amazon Associate:
   http://docs.aws.amazon.com/AWSECommerceService/latest/DG/becomingAssociate.html


Notes
=====

Some parts of this module are based on Sebastian Rahlf's
`python-amazon-product-api`_.

.. _python-amazon-product-api:
   https://bitbucket.org/basti/python-amazon-product-api
