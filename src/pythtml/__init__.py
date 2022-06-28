# -*- coding: utf-8 -*-

"""
pythtml is an alternative to templates that implements HTML 5 documents in Python code.
It is not an HTML parser/validator; it assumes that user has some knowledge of HTML.
"""

try:
    from importlib.metadata import metadata  # type: ignore
except ImportError:
    from importlib_metadata import metadata  # type: ignore

from .elements import *

__version__: str = metadata(__name__)["version"]
