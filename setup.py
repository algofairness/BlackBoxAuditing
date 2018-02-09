#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from codecs import open
import os, sys 

here = os.path.abspath(os.path.dirname(__file__))

if sys.version_info[0] == 3:
    source_dir = '.'
else:
    source_dir = 'python2_source'

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

NAME ='blackboxauditing'
VERSION = '0.1.27'

DESCRIPTION = 'Sample Implementation of Gradient Feature Auditing (GFA)'
LONG_DESCRIPTION = long_description

URL = 'https://github.com/algofairness/BlackBoxAuditing'
AUTHOR ='Philip Adler, Casey Falk, Sorelle A. Friedler, Gabriel Rybeck, Carlos Scheidegger, Brandon Smith, Suresh Venkatasubramanian, Michael Feldman, John Moeller, Derek Roth, Charlie Marx'
AUTHOR_EMAIL='fairness@haverford.edu'
LICENSE='Apache 2.0'

CLASSIFIERS = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Topic :: Software Development',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 2.7',
  'Programming Language :: Python :: 3.0',
]
KEYWORDS = 'algorithmic fairness'

PACKAGES = find_packages()
PACKAGE_DATA = {
  'BlackBoxAuditing': ['*.sh','r_plotting/*.Rmd', 'repair_tests/*.csv', 'MATLAB_code/*'],
  'BlackBoxAuditing.test_data': ['*.csv', '*.arff']
}
INCLUDE_PACKAGE_DATA = True
PACKAGE_DIR = {
  '': source_dir,
}

INSTALL_REQUIRES = [
  'networkx',
  'matplotlib',
  'Orange3']

CMDCLASS = {
}

ENTRY_POINTS = {
  'console_scripts': [
    'BlackBoxAuditing-test = BlackBoxAuditing.test:test',
    'BlackBoxAuditing-repair = BlackBoxAuditing.repair:main',
  ],
}

setup(
  name=NAME,
  version=VERSION,
  description=DESCRIPTION,
  long_description=LONG_DESCRIPTION,
  url=URL,
  author=AUTHOR,
  author_email=AUTHOR_EMAIL,
  license=LICENSE,
  classifiers=CLASSIFIERS,
  keywords=KEYWORDS,
  packages=PACKAGES,
  package_data=PACKAGE_DATA,
  include_package_data=INCLUDE_PACKAGE_DATA,
  package_dir = PACKAGE_DIR,
  install_requires=INSTALL_REQUIRES,
  cmdclass=CMDCLASS,
  entry_points=ENTRY_POINTS
)

    

    

     


