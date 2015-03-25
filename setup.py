# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

# unicode_literals is omitted from the import above because setuptools.setup does not like 
# a unicode string in the packages argument.


import io
from setuptools import setup
from setuptools.command.test import test as TestCommand
import json
import string


class Tox(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        #import here, cause outside the eggs aren't loaded
        import tox
        errcode = tox.cmdline(self.test_args)
        sys.exit(errcode)


def package_version():
    with io.open('pyfive/__init__.py', 'r', encoding='utf-8') as f:
        for sourceline in f:
            if sourceline.strip().startswith('__version__'):
                 return sourceline.split('=', 1)[1].strip(string.whitespace + '"\'')
        else:
            raise Exception('Unable to read package version.')


setup(name='pyfive',
    version=package_version(),
    author='Charles Yeomans', 
    packages=['pyfive'],
    cmdclass = {'test': Tox}
    )
      
      