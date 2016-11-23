from setuptools import setup, find_packages


setup(name='amzn-api',
      version='0.1.0',
      description='Amazon Product Advertising API',
      url='https://github.com/rrranthony/amzn-api',
      author='Anthony Young',
      author_email='ayoung87@gmail.com',
      # find_packages includes subpackages automatically
      packages=find_packages(),
      # Run-time dependencies.  These get installed by pip when this project is installed.
      # requirements.txt should included these, as well any requirements for development and testing
      # (e.g., pytest, coverage).
      install_requires=[
          'requests',
          'xmltodict',
      ],
)
