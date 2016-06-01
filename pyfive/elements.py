# -*- coding: utf-8 -*-

"""pyfive elements."""

from __future__ import absolute_import, unicode_literals, division, print_function

import sys
try:
    from html import escape
except ImportError:
    from cgi import escape

from xml.sax.saxutils import quoteattr
from functools import partial
from keyword import kwlist


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
    text = unicode if is2 else str # pylint: disable=undefined-variable
    bytes = str if is2 else bytes

    def __init__(self, *args, **kwargs):
        super(_BaseElement, self).__init__(*args, **kwargs)

    def textify(self, value):
        """Takes the argument s and returns a unicode object.  Intended to work on anything
        that supports conversion to string; e.g. int, bool, uuid."""

        if isinstance(value, self.text):
            return value
        else:
            return value.decode(self.ENCODING) if hasattr(value, 'decode') else self.text(value)



class _Element(_BaseElement):
    """Implements HTML element functions."""

    # used for attribute names.
    kwmap = {u'%s_' % kw: _BaseElement.text(kw) for kw in kwlist}

    def __init__(self, element_name, is_empty, *children, **attributes):
        # Name clashes with keywords are resolved by appending _ as suggested by PEP 8.
        # Attribute names beginning with 'data_' are presumed to be HTML5 data-* attribute
        # names, and so underscores are replaced with dashes.

        super(_Element, self).__init__()

        self.name = element_name
        self.is_empty = is_empty

        self.children = [escape(self.textify(x)) if isinstance(x, (self.text, self.bytes)) #pylint: disable=deprecated-method
            else x for x in children if x is not None]

        # strip attributes having value None or False
        self.attributes = {self._attr_name(k) : self._attr_value(v)
            for k, v in attributes.items()
            if v not in (None, False)
            }

    def _attr_name(self, name):
        """ Implements attribute name conventions."""

        name = self.textify(name)
        return name.replace(u'_', u'-') if name.startswith(u'data_') else self.kwmap.get(name, name)

    def _attr_value(self, value):
        """Returns quoted attribute value."""

        return value if isinstance(value, bool) else quoteattr(self.textify(value))

    def _generate_attrs(self):
        """ Generates attribute strings."""

        #if isinstance(attr_value, bool), then I assume that __init__ filtered out attributes.
        # with value False.
        return u' '.join([attr_name if isinstance(attr_value, bool)
            else '%s=%s' % (attr_name, attr_value)
            for attr_name, attr_value in self.attributes.items()])

    def __unicode__(self):
        if self.is_empty:
            return u'<%s%s%s>' % (self.name, ' ' if self.attributes else '', self._generate_attrs())
        else:
            return (u'<!DOCTYPE html>\n<%s%s%s>%s</%s>'
                if self.name == u'html' else u'<%s%s%s>%s</%s>') % (
                self.name,
                ' ' if self.attributes else '',
                self._generate_attrs(),
                ''.join([child.__unicode__() for child in self.children]),
                self.name
                )

    def __bytes__(self):
        return self.__unicode__().encode(self.ENCODING)

    def __str__(self):
        return self.__bytes__() if self.is2 else self.__unicode__()




class _ElementRaw(_BaseElement):
    """Implements the raw function."""

    def __init__(self, data, *args, **kwargs):
        """Wraps a string that should not be escaped; e.g. javaascript code, or an HTML
        element already rendered as a string.

        :data: a str | unicode | bytes object.
        """

        super(_ElementRaw, self).__init__(*args, **kwargs)
        self.data = self.textify(data)

    def __unicode__(self):
        # should only be invoked in python 2.
        return self.data

    def __bytes__(self):
        # should only be invoked in python 3, but I'll handle both versions anyway.
        return self.data.encode(self.ENCODING)

    def __str__(self):
        return self.__bytes__()


#pylint: disable=invalid-name
raw = _ElementRaw

for element_type, is_empty_element in ELEMENTS:
    setattr(sys.modules[__name__], element_type, partial(_Element, element_type, is_empty_element))
