# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, division, print_function

import sys
import cgi
from xml.sax.saxutils import quoteattr
from keyword import iskeyword
from functools import partial



#element = (name, is_empty_element)
ELEMENTS = [
    ('a', False),
    ('abbr', False),
    ('acronym', False),
    ('address', False),
    ('area', True),
    ('article', False),
    ('audio', False),
    ('b', False),
    ('base', True),
    ('bdi', False),
    ('bdo', False),
    ('big', False),
    ('blockquote', False),
    ('body', False),
    ('br', True),
    ('button', False),
    ('canvas', False),
    ('caption', False),
    ('cite', False),
    ('code', False),
    ('col', True),
    ('colgroup', False),
    ('data', False),
    ('datalist', False),
    ('dd', False),
    ('del', False),
    ('details', False),
    ('dfn', False),
    ('dialog', False),
    ('div', False),
    ('dl', False),
    ('dt', False),
    ('em', False),
    ('embed', True),
    ('fieldset', False),
    ('footer', False),
    ('form', False),
    ('frame', True),
    ('frameset', False),
    ('h1', False),
    ('h2', False),
    ('h3', False),
    ('h4', False),
    ('h5', False),
    ('h6', False),
    ('head', False),
    ('header', False),
    ('hr', True),
    ('html', False),
    ('i', False),
    ('iframe', False),
    ('img', True),
    ('input', True),
    ('ins', False),
    ('keygen', True),
    ('kbd', False),
    ('label', False),
    ('legend', False),
    ('li', False),
    ('link', True),
    ('meta', True),
    ('meter', False),
    ('map', False),
    ('noframes', False),
    ('noscript', False),
    ('object', False),
    ('ol', False),
    ('optgroup', False),
    ('option', False),
    ('output', False),
    ('p', False),
    ('param', True),
    ('pre', False),
    ('progress', False),
    ('rp', False),
    ('rt', False),
    ('ruby', False),
    ('q', False),
    ('samp', False),
    ('script', False),
    ('select', False),
    ('small', False),
    ('source', True),
    ('span', False),
    ('strong', False),
    ('style', False),
    ('sub', False),
    ('summary', False),
    ('sup', False),
    ('table', False),
    ('tbody', False),
    ('td', False),
    ('textarea', False),
    ('tfoot', False),
    ('th', False),
    ('thead', False),
    ('time', False),
    ('title', False),
    ('tr', False),
    ('track', True),
    ('tt', False),
    ('ul', False),
    ('var', False),
    ('video', False),
    ('wbr', True)
    ]


__all__ = [x[0] for x in ELEMENTS] + ['raw']

#pylint: disable=too-few-public-methods
class _BaseElement(object):
    """
    Implements the str/unicode functionality for Element classes.
    pyfive prefers Unicode input.  If you pass strings, they are assumed to be UTF-8.
    """

    ENCODING = 'utf-8'
    is2 = sys.version_info.major == 2
    text = unicode if is2 else str
    bytes = str if is2 else bytes

    def __init__(self, *args, **kwargs):
        super(_BaseElement, self).__init__(*args, **kwargs)
        self.data = None

    #pylint: disable=invalid-name
    def u_ensure(self, s):
        """Takes the argument s and returns a unicode object."""

        if isinstance(s, self.text):
            return s
        else:
            return s.decode(self.ENCODING) if hasattr(s, 'decode') else self.text(s)

    def __unicode__(self):
        # should only be invoked in python 2.
        return self.data

    def __str__(self):
        return self.data.encode(self.ENCODING) if self.is2 else self.data

    def __bytes__(self):
        # should only be invoked in python 3, but I'll handle both versions anyway.
        return self.data.encode(self.ENCODING) if not self.is2 else self.__str__()


class _Element(_BaseElement):
    """Implements HTML element functions."""

    def __init__(self, name, is_empty, *children, **attributes):
        super(_Element, self).__init__()
        #pylint: disable=redefined-outer-name
        _children = [cgi.escape(self.u_ensure(x)) if isinstance(x, (self.text, self.bytes)) else self.text(x) for x in children]
        self.data = self.generate_html(name, is_empty, _children, self.generate_attrs(attributes))

    def fix_attr_name(self, name):
        # Name clashes with keywords can be resolved by
        # capitalizing the attribute parameter name.
        # Attribute names beginning with 'data_' are presumed to be HTML5 data-* attribute
        # names, and so underscores are replaced with dashes.

        name = self.u_ensure(name)
        return name.replace('_', '-') if name.startswith('data_') else name[0].lower() + name[1:] if iskeyword(name[0].lower() + name[1:]) else name

    def fix_attr_value(self, value):
        return value if isinstance(value, bool) else quoteattr(self.u_ensure(value))

    def generate_attrs(self, attributes):
        attrs = [(attr_name, attr_value) for attr_name, attr_value in attributes.items() if not isinstance(attr_value, bool) or attr_value == True]
        attrs = [(self.fix_attr_name(attr_name), attr_value if isinstance(attr_value, bool) else self.fix_attr_value(attr_value)) for attr_name, attr_value in attrs]
        return ' '.join([(attr_name if attr_value else '') if isinstance(attr_value, bool) else '%s=%s' % (attr_name, attr_value) for attr_name, attr_value in attrs])

    @staticmethod
    def generate_html(name, is_empty, children, attributes):
        if is_empty:
            return '<%s%s%s>' % (name, ' ' if attributes else '', attributes)
        else:
            return ('<!DOCTYPE html>\n<%s%s%s>%s</%s>' if name == 'html' else '<%s%s%s>%s</%s>') % (name, ' ' if attributes else '', attributes, ''.join(children), name)


class _ElementRaw(_BaseElement):
    """Implements the raw function."""

    def __init__(self, data):
        super(_ElementRaw, self).__init__()
        self.data = self.u_ensure(data)


#pylint: disable=invalid-name
raw = _ElementRaw

for element_name, is_empty_element in ELEMENTS:
    setattr(sys.modules[__name__], element_name, partial(_Element, element_name, is_empty_element))
