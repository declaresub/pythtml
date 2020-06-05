# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

# unicode_literals is omitted from the import above because setuptools.setup does not like 
# a unicode string in the packages argument.



from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


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


setup(name='pyfive',
    author='Charles Yeomans', 
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    keywords=['web', 'html'],
    cmdclass = {'test': Tox},
    extras_require={':python_version < "3.8"': ["importlib_metadata"]},
    include_package_data=True,
    zip_safe=False,
    options={"bdist_wheel": {"universal": "1"}},
    )
      
      