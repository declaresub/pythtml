# -*- coding: utf-8 -*-

"""pyfive elements."""

from __future__ import absolute_import, unicode_literals, division, print_function

import sys
try:
    from html import escape
except ImportError:
    from cgi import escape

from xml.sax.saxutils import quoteattr
from keyword import kwlist


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

    def __init__(self):
        super(_BaseElement, self).__init__()

    def textify(self, value):
        """Takes the argument s and returns a unicode object.  Intended to work on anything
        that supports conversion to string; e.g. int, bool, uuid."""

        if isinstance(value, self.text):
            return value
        else:
            return value.decode(self.ENCODING) if hasattr(value, 'decode') else self.text(value)


class _Element(_BaseElement):
    """Implements HTML element functions."""

    # these attributes must be set in subclasses.
    tag = None
    is_empty = False

    # used for attribute names.
    kwmap = {u'%s_' % kw: _BaseElement.text(kw) for kw in kwlist}

    def __init__(self, *children, **attributes):
        # Name clashes with keywords are resolved by appending _ as suggested by PEP 8.
        # For example to pass a class attribute as a keyword argument, use
        # class_'foo, bar'.  The trailing underscore will be stripped because 'class' is a
        # keyword, and a class attribute will be added.
        # Attribute names beginning with 'data_' are presumed to be HTML5 data-* attribute
        # names, and so underscores are replaced with dashes.

        super(_Element, self).__init__()
        self._children = []

        for child in children:
            self.append(child)

        # strip attributes having value None or False
        self.attributes = {self._attr_name(k) : v
            for k, v in attributes.items()
            if v not in (None, False)
            }

    def _attr_name(self, name):
        """ Implements attribute name conventions."""

        name = self.textify(name)
        return name.replace(u'_', u'-') if name.startswith(u'data_') else self.kwmap.get(name, name)

    def _generate_attrs(self):
        """ Generates attribute strings."""

        #if isinstance(attr_value, bool), then I assume that __init__ filtered out attributes.
        # with value False.
        return u' '.join([attr_name if isinstance(attr_value, bool)
            else '%s=%s' % (attr_name, quoteattr(self.textify(attr_value)))
            for attr_name, attr_value in self.attributes.items()])

    def __unicode__(self):
        if self.is_empty:
            return u'<%s%s%s>' % (self.tag, ' ' if self.attributes else '', self._generate_attrs())
        else:
            return (u'<!DOCTYPE html>\n<%s%s%s>%s</%s>'
                if self.tag == u'html' else u'<%s%s%s>%s</%s>') % (
                self.tag,
                ' ' if self.attributes else '',
                self._generate_attrs(),
                ''.join([child if isinstance(child, self.text) else child.__unicode__() for child in self._children]),
                self.tag
                )

    def __bytes__(self):
        return self.__unicode__().encode(self.ENCODING)

    def __str__(self):
        return self.__bytes__() if self.is2 else self.__unicode__()

    def children(self, tag=None):
        """Returns a list of all children in the order added.
        If tag is not None, then the list is filtered by tag."""
        
        return [x for x in self._children if tag is None or getattr(x, 'tag', None) == tag]

    def append(self, child):
        """Appends child element."""

        if child is None:
            return

        self._children.append(child if isinstance(child, _BaseElement) #pylint: disable=deprecated-method
            else escape(self.textify(child), quote=False))

    def remove(self, child):
        """Removes child element from children, if present."""

        self._children = [x for x in self._children if x != child]

    def find_by_id(self, value):
        """Finds the element in the tree having attribute id="value", if present.
        Some so-called "full stack developers" think it's okay to have multiple elements
        with the same id value. This method does not support that."""

        if self.attributes.get('id') == value:
            return self
        else:
            for child in self._children:
                element = child.find_by_id(value) if hasattr(child, 'find_by_id') else None
                if element:
                    break
            else:
                element = None
            return element


class Raw(_BaseElement):
    """Implements the raw function."""

    def __init__(self, data, *args, **kwargs):
        """Wraps a string that should not be escaped; e.g. javaascript code, or an HTML
        element already rendered as a string.

        :data: a str | unicode | bytes object.
        """

        super(Raw, self).__init__(*args, **kwargs)
        self.data = self.textify(data)

    def __unicode__(self):
        # should only be invoked in python 2.
        return self.data

    def __bytes__(self):
        # should only be invoked in python 3, but I'll handle both versions anyway.
        return self.data.encode(self.ENCODING)

    def __str__(self):
        return self.__bytes__()


# HTML element subclasses.


class A(_Element): # pylint: disable=invalid-name
    """Represents an HTML a element."""
    
    tag = 'a'


class Abbr(_Element):
    """Represents an HTML abbr element."""

    tag = 'abbr'


class Acronym(_Element):
    """Represents an HTML acronym element."""

    tag = 'acronym'


class Address(_Element):
    """Represents an HTML address element."""

    tag = 'address'


class Area(_Element):
    """Represents an HTML area element."""

    tag = 'area'
    is_empty = True

class Article(_Element):
    """Represents an HTML article element."""

    tag = 'article'


class Audio(_Element):
    """Represents an HTML audio element."""

    tag = 'audio'


class B(_Element): # pylint: disable=invalid-name
    """Represents an HTML b element."""

    tag = 'b'


class Base(_Element):
    """Represents an HTML base element."""

    tag = 'base'


class Bdi(_Element):
    """Represents an HTML bdi element."""

    tag = 'bdi'

class Bdo(_Element):
    """Represents an HTML bdo element."""

    tag = 'bdo'

class Big(_Element):
    """Represents an HTML big element."""

    tag = 'big'


class Blockquote(_Element):
    """Represents an HTML blockquote element."""

    tag = 'blockquote'


class Body(_Element):
    """Represents an HTML body element."""

    tag = 'body'


class Br(_Element):
    """Represents an HTML br element."""

    tag = 'br'


class Button(_Element):
    """Represents an HTML button element."""

    tag = 'button'


class Canvas(_Element):
    """Represents an HTML canvas element."""

    tag = 'canvas'


class Caption(_Element):
    """Represents an HTML caption element."""

    tag = 'caption'


class Cite(_Element):
    """Represents an HTML cite element."""

    tag = 'cite'


class Code(_Element):
    """Represents an HTML code element."""

    tag = 'code'


class Col(_Element):
    """Represents an HTML col element."""

    tag = 'col'
    is_empty = True


class Colgroup(_Element):
    """Represents an HTML colgroup element."""

    tag = 'colgroup'


class Data(_Element):
    """Represents an HTML data element."""

    tag = 'data'


class Datalist(_Element):
    """Represents an HTML datalist element."""

    tag = 'datalist'


class Dd(_Element):
    """Represents an HTML dd element."""

    tag = 'dd'


class Del(_Element):
    """Represents an HTML del element."""

    tag = 'del'


class Details(_Element):
    """Represents an HTML details element."""

    tag = 'details'


class Dfn(_Element):
    """Represents an HTML dfn element."""

    tag = 'dfn'


class Dialog(_Element):
    """Represents an HTML dialog element."""

    tag = 'dialog'


class Div(_Element):
    """Represents an HTML div element."""

    tag = 'div'


class Dl(_Element):
    """Represents an HTML dl element."""

    tag = 'dl'


class Dt(_Element):
    """Represents an HTML dt element."""

    tag = 'dt'


class Em(_Element):
    """Represents an HTML em element."""

    tag = 'em'


class Embed(_Element):
    """Represents an HTML embed element."""

    tag = 'embed'
    is_empty = True


class Fieldset(_Element):
    """Represents an HTML fieldset element."""

    tag = 'fieldset'


class Footer(_Element):
    """Represents an HTML footer element."""

    tag = 'footer'


class Form(_Element):
    """Represents an HTML form element."""

    tag = 'form'

class Frame(_Element):
    """Represents an HTML frame element."""

    tag = 'frame'
    is_empty = True


class Frameset(_Element):
    """Represents an HTML frameset element."""

    tag = 'frameset'


class H1(_Element):
    """Represents an HTML h1 element."""

    tag = 'h1'


class H2(_Element):
    """Represents an HTML h2 element."""

    tag = 'h2'


class H3(_Element):
    """Represents an HTML h3 element."""

    tag = 'h3'


class H4(_Element):
    """Represents an HTML h4 element."""

    tag = 'h4'


class H5(_Element):
    """Represents an HTML h5 element."""

    tag = 'h5'


class H6(_Element):
    """Represents an HTML h6 element."""

    tag = 'h6'


class Head(_Element):
    """Represents an HTML head element."""

    tag = 'head'


class Header(_Element):
    """Represents an HTML header element."""

    tag = 'header'


class Hr(_Element):
    """Represents an HTML hr element."""

    tag = 'hr'


class Html(_Element):
    """Represents an HTML html element."""

    tag = 'html'


    def body(self):
        "Returns the body child element, if present, or None."""

        body_list = self.children(tag='body')
        return body_list[0] if len(body_list) > 0 else None

    def head(self):
        "Returns the head child element, if present, or None."""

        head_list = self.children(tag='head')
        return head_list[0] if len(head_list) > 0 else None

class I(_Element): # pylint: disable=invalid-name
    """Represents an HTML i element."""

    tag = 'i'


class Iframe(_Element):
    """Represents an HTML iframe element."""

    tag = 'iframe'


class Img(_Element):
    """Represents an HTML img element."""

    tag = 'img'
    is_empty = True


class Input(_Element):
    """Represents an HTML input element."""

    tag = 'input'
    is_empty = True


class Ins(_Element):
    """Represents an HTML ins element."""

    tag = 'ins'


class Keygen(_Element):
    """Represents an HTML keygen element."""

    tag = 'keygen'


class Kbd(_Element):
    """Represents an HTML kbd element."""

    tag = 'kbd'


class Label(_Element):
    """Represents an HTML label element."""

    tag = 'label'

class Legend(_Element):
    """Represents an HTML legend element."""

    tag = 'legend'


class Li(_Element):
    """Represents an HTML li element."""

    tag = 'li'


class Link(_Element):
    """Represents an HTML link element."""

    tag = 'link'
    is_empty = True


class Meta(_Element):
    """Represents an HTML meta element."""

    tag = 'meta'
    is_empty = True


class Meter(_Element):
    """Represents an HTML meter element."""

    tag = 'meter'
    is_empty = True


class Map(_Element):
    """Represents an HTML map element."""

    tag = 'map'


class Noframes(_Element):
    """Represents an HTML noframes element."""

    tag = 'noframes'


class Noscript(_Element):
    """Represents an HTML noscript element."""

    tag = 'noscript'


class Object(_Element):
    """Represents an HTML object element."""

    tag = 'object'


class Ol(_Element):
    """Represents an HTML ol element."""

    tag = 'ol'


class Optgroup(_Element):
    """Represents an HTML optgroup element."""

    tag = 'optgroup'


class Option(_Element):
    """Represents an HTML option element."""

    tag = 'option'


class Output(_Element):
    """Represents an HTML output element."""

    tag = 'output'


class P(_Element): # pylint: disable=invalid-name
    """Represents an HTML p element."""

    tag = 'p'


class Param(_Element):
    """Represents an HTML param element."""

    tag = 'param'
    is_empty = True


class Pre(_Element):
    """Represents an HTML pre element."""

    tag = 'pre'


class Progress(_Element):
    """Represents an HTML progress element."""

    tag = 'progress'


class Rp(_Element):
    """Represents an HTML rp element."""

    tag = 'rp'


class Rt(_Element):
    """Represents an HTML rt element."""

    tag = 'rt'


class Ruby(_Element):
    """Represents an HTML ruby element."""

    tag = 'ruby'


class Q(_Element): # pylint: disable=invalid-name
    """Represents an HTML q element."""

    tag = 'q'


class Samp(_Element):
    """Represents an HTML samp element."""

    tag = 'samp'


class Script(_Element):
    """Represents an HTML script element."""

    tag = 'script'


class Select(_Element):
    """Represents an HTML select element."""

    tag = 'select'


class Small(_Element):
    """Represents an HTML small element."""

    tag = 'small'


class Source(_Element):
    """Represents an HTML source element."""

    tag = 'source'
    is_empty = True


class Span(_Element):
    """Represents an HTML span element."""

    tag = 'span'


class Strong(_Element):
    """Represents an HTML strong element."""

    tag = 'strong'


class Style(_Element):
    """Represents an HTML style element."""

    tag = 'style'


class Sub(_Element):
    """Represents an HTML sub element."""

    tag = 'sub'


class Summary(_Element):
    """Represents an HTML summary element."""

    tag = 'summary'


class Sup(_Element):
    """Represents an HTML sup element."""

    tag = 'sup'


class Table(_Element):
    """Represents an HTML table element."""

    tag = 'table'


class Tbody(_Element):
    """Represents an HTML tbody element."""

    tag = 'tbody'


class Td(_Element):
    """Represents an HTML td element."""

    tag = 'td'


class Textarea(_Element):
    """Represents an HTML textarea element."""

    tag = 'textarea'


class Tfoot(_Element):
    """Represents an HTML tfoot element."""

    tag = 'tfoot'


class Th(_Element):
    """Represents an HTML th element."""

    tag = 'th'


class Thead(_Element):
    """Represents an HTML thead element."""

    tag = 'thead'


class Time(_Element):
    """Represents an HTML time element."""

    tag = 'time'


class Title(_Element):
    """Represents an HTML title element."""

    tag = 'title'


class Tr(_Element):
    """Represents an HTML tr element."""

    tag = 'tr'


class Track(_Element):
    """Represents an HTML track element."""

    tag = 'track'
    is_empty = True


class Tt(_Element):
    """Represents an HTML tt element."""

    tag = 'tt'


class Ul(_Element):
    """Represents an HTML ul element."""

    tag = 'ul'


class Var(_Element):
    """Represents an HTML var element."""

    tag = 'var'


class Video(_Element):
    """Represents an HTML video element."""

    tag = 'video'


class Wbr(_Element):
    """Represents an HTML wbr element."""

    tag = 'wbr'
    is_empty = True




# The python code used to generate the element subclass definitions

# ELEMENTS = [
#     ('a', False),
#     ('abbr', False),
#     ('acronym', False),
#     ('address', False),
#     ('area', True),
#     ('article', False),
#     ('audio', False),
#     ('b', False),
#     ('base', True),
#     ('bdi', False),
#     ('bdo', False),
#     ('big', False),
#     ('blockquote', False),
#     ('body', False),
#     ('br', True),
#     ('button', False),
#     ('canvas', False),
#     ('caption', False),
#     ('cite', False),
#     ('code', False),
#     ('col', True),
#     ('colgroup', False),
#     ('data', False),
#     ('datalist', False),
#     ('dd', False),
#     ('del', False),
#     ('details', False),
#     ('dfn', False),
#     ('dialog', False),
#     ('div', False),
#     ('dl', False),
#     ('dt', False),
#     ('em', False),
#     ('embed', True),
#     ('fieldset', False),
#     ('footer', False),
#     ('form', False),
#     ('frame', True),
#     ('frameset', False),
#     ('h1', False),
#     ('h2', False),
#     ('h3', False),
#     ('h4', False),
#     ('h5', False),
#     ('h6', False),
#     ('head', False),
#     ('header', False),
#     ('hr', True),
#     ('html', False),
#     ('i', False),
#     ('iframe', False),
#     ('img', True),
#     ('input', True),
#     ('ins', False),
#     ('keygen', True),
#     ('kbd', False),
#     ('label', False),
#     ('legend', False),
#     ('li', False),
#     ('link', True),
#     ('meta', True),
#     ('meter', False),
#     ('map', False),
#     ('noframes', False),
#     ('noscript', False),
#     ('object', False),
#     ('ol', False),
#     ('optgroup', False),
#     ('option', False),
#     ('output', False),
#     ('p', False),
#     ('param', True),
#     ('pre', False),
#     ('progress', False),
#     ('rp', False),
#     ('rt', False),
#     ('ruby', False),
#     ('q', False),
#     ('samp', False),
#     ('script', False),
#     ('select', False),
#     ('small', False),
#     ('source', True),
#     ('span', False),
#     ('strong', False),
#     ('style', False),
#     ('sub', False),
#     ('summary', False),
#     ('sup', False),
#     ('table', False),
#     ('tbody', False),
#     ('td', False),
#     ('textarea', False),
#     ('tfoot', False),
#     ('th', False),
#     ('thead', False),
#     ('time', False),
#     ('title', False),
#     ('tr', False),
#     ('track', True),
#     ('tt', False),
#     ('ul', False),
#     ('var', False),
#     ('video', False),
#     ('wbr', True)
#     ]
#
#
# class_template = """class %(cls)s(_Element):
#     \"\"\"Represents an HTML %(tag)s element.\"\"\"
#
#     def __init__(self, *children, **attributes):
#         super(%(cls)s, self).__init__('%(tag)s', %(is_empty)s, *children, **attributes)"""
#
# for tag, is_empty in ELEMENTS:
#     print class_template % dict(cls=tag.title(), tag=tag, is_empty=is_empty)
#     print ''

