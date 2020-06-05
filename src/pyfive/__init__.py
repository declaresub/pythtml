# -*- coding: utf-8 -*-

"""
pyfive is an alternative to templates that implements HTML 5 documents in Python code.
It is not an HTML parser/validator; it assumes that user has some knowledge of HTML.
"""

try:
    from importlib.metadata import metadata, PackageNotFoundError
except ImportError:
    from importlib_metadata import metadata, PackageNotFoundError

from .elements import * #pylint: disable=wildcard-import


__version__ = metadata(__name__)['version']
