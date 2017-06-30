#!/usr/bin/env python

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from codecs import open
import os 

here = os.path.abspath(os.path.dirname(__file__))


class PostDevelopCommand(develop):
  """Post-installation for development mode."""
  def run(self):
    # Find path to weka.jar
    def find(name, path):
      for root, dirs, files in os.walk(path):
        if name in files:
          return os.path.join(root, name)
 
    # Update WEKA_PATH
    WEKA_PATH = find("weka.jar",'/')
    file_location = 'BlackBoxAuditing/model_factories/weka.path'
    with open(os.path.join(here, file_location), 'w') as f:
      f.write(WEKA_PATH)

    develop.run(self)

class PostInstallCommand(install):
  """Post-installation for installation mode."""
  def run(self):
    # Find path to weka.jar
    def find(name, path):
      for root, dirs, files in os.walk(path):
        if name in files:
          return os.path.join(root, name)

    # Update WEKA_PATH
    WEKA_PATH = find("weka.jar",'/')
    file_location = 'BlackBoxAuditing/model_factories/weka.path'
    with open(os.path.join(here, file_location), 'w') as f:
      f.write(WEKA_PATH)    

    install.run(self)

with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

NAME ='BlackBoxAuditing'
VERSION = '0.0.1'

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
]
KEYWORDS = 'algorithmic fairness'

PACKAGES = find_packages()
PACKAGE_DATA = {
  'BlackBoxAuditing': ['*.sh','r_plotting/*.Rmd', 'repair_tests/*.csv', 'MATLAB_code/*'],
  'BlackBoxAuditing.test_data': ['*.csv', '*.arff'],
  'BlackBoxAuditing.model_factories': ['weka.path'],
}
INCLUDE_PACKAGE_DATA = True

INSTALL_REQUIRES = [
  'tensorflow',
  'weka']

CMDCLASS = {
  'develop': PostDevelopCommand,
  'install': PostInstallCommand,
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
  install_requires=INSTALL_REQUIRES,
  cmdclass=CMDCLASS,
  entry_points=ENTRY_POINTS
)

    

    

     


