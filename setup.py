from setuptools import setup, find_packages


setup(name='amzn-api',
      version='0.1.0',
      description='Amazon Product Advertising API',
      url='https://github.com/rrranthony/amzn-api',
      author='Anthony Young',
      author_email='ayoung87@gmail.com',
      packages=find_packages(),
      scripts=[
          'amzn/bin/amazon_item_lookup',
          'amzn/bin/print_cached_raw_item_lookup_xml'
      ],
      install_requires=[
          'requests==2.13.0',
          'xmltodict==0.10.2',
      ],
)
