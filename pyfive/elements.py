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

    # used for attribute names.
    kwmap = {u'%s_' % kw: _BaseElement.text(kw) for kw in kwlist}

    def __init__(self, tag, is_empty, *children, **attributes):
        # Name clashes with keywords are resolved by appending _ as suggested by PEP 8.
        # For example to pass a class attribute as a keyword argument, use
        # class_'foo, bar'.  The trailing underscore will be stripped because 'class' is a
        # keyword, and a class attribute will be added.
        # Attribute names beginning with 'data_' are presumed to be HTML5 data-* attribute
        # names, and so underscores are replaced with dashes.

        super(_Element, self).__init__()

        self.tag = tag
        self.is_empty = is_empty
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

        return [x for x in self._children if tag is None or x.tag == tag]

    def append(self, child):
        """Appends child element."""

        if child is None:
            return

        self._children.append(escape(self.textify(child), quote=False) #pylint: disable=deprecated-method
            if isinstance(child, (self.text, self.bytes)) else child)

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

    def __init__(self, *children, **attributes):
        super(A, self).__init__('a', False, *children, **attributes)

class Abbr(_Element):
    """Represents an HTML abbr element."""

    def __init__(self, *children, **attributes):
        super(Abbr, self).__init__('abbr', False, *children, **attributes)

class Acronym(_Element):
    """Represents an HTML acronym element."""

    def __init__(self, *children, **attributes):
        super(Acronym, self).__init__('acronym', False, *children, **attributes)

class Address(_Element):
    """Represents an HTML address element."""

    def __init__(self, *children, **attributes):
        super(Address, self).__init__('address', False, *children, **attributes)

class Area(_Element):
    """Represents an HTML area element."""

    def __init__(self, *children, **attributes):
        super(Area, self).__init__('area', True, *children, **attributes)

class Article(_Element):
    """Represents an HTML article element."""

    def __init__(self, *children, **attributes):
        super(Article, self).__init__('article', False, *children, **attributes)

class Audio(_Element):
    """Represents an HTML audio element."""

    def __init__(self, *children, **attributes):
        super(Audio, self).__init__('audio', False, *children, **attributes)

class B(_Element): # pylint: disable=invalid-name
    """Represents an HTML b element."""

    def __init__(self, *children, **attributes):
        super(B, self).__init__('b', False, *children, **attributes)

class Base(_Element):
    """Represents an HTML base element."""

    def __init__(self, *children, **attributes):
        super(Base, self).__init__('base', True, *children, **attributes)

class Bdi(_Element):
    """Represents an HTML bdi element."""

    def __init__(self, *children, **attributes):
        super(Bdi, self).__init__('bdi', False, *children, **attributes)

class Bdo(_Element):
    """Represents an HTML bdo element."""

    def __init__(self, *children, **attributes):
        super(Bdo, self).__init__('bdo', False, *children, **attributes)

class Big(_Element):
    """Represents an HTML big element."""

    def __init__(self, *children, **attributes):
        super(Big, self).__init__('big', False, *children, **attributes)

class Blockquote(_Element):
    """Represents an HTML blockquote element."""

    def __init__(self, *children, **attributes):
        super(Blockquote, self).__init__('blockquote', False, *children, **attributes)

class Body(_Element):
    """Represents an HTML body element."""

    def __init__(self, *children, **attributes):
        super(Body, self).__init__('body', False, *children, **attributes)

class Br(_Element):
    """Represents an HTML br element."""

    def __init__(self, *children, **attributes):
        super(Br, self).__init__('br', True, *children, **attributes)

class Button(_Element):
    """Represents an HTML button element."""

    def __init__(self, *children, **attributes):
        super(Button, self).__init__('button', False, *children, **attributes)

class Canvas(_Element):
    """Represents an HTML canvas element."""

    def __init__(self, *children, **attributes):
        super(Canvas, self).__init__('canvas', False, *children, **attributes)

class Caption(_Element):
    """Represents an HTML caption element."""

    def __init__(self, *children, **attributes):
        super(Caption, self).__init__('caption', False, *children, **attributes)

class Cite(_Element):
    """Represents an HTML cite element."""

    def __init__(self, *children, **attributes):
        super(Cite, self).__init__('cite', False, *children, **attributes)

class Code(_Element):
    """Represents an HTML code element."""

    def __init__(self, *children, **attributes):
        super(Code, self).__init__('code', False, *children, **attributes)

class Col(_Element):
    """Represents an HTML col element."""

    def __init__(self, *children, **attributes):
        super(Col, self).__init__('col', True, *children, **attributes)

class Colgroup(_Element):
    """Represents an HTML colgroup element."""

    def __init__(self, *children, **attributes):
        super(Colgroup, self).__init__('colgroup', False, *children, **attributes)

class Data(_Element):
    """Represents an HTML data element."""

    def __init__(self, *children, **attributes):
        super(Data, self).__init__('data', False, *children, **attributes)

class Datalist(_Element):
    """Represents an HTML datalist element."""

    def __init__(self, *children, **attributes):
        super(Datalist, self).__init__('datalist', False, *children, **attributes)

class Dd(_Element):
    """Represents an HTML dd element."""

    def __init__(self, *children, **attributes):
        super(Dd, self).__init__('dd', False, *children, **attributes)

class Del(_Element):
    """Represents an HTML del element."""

    def __init__(self, *children, **attributes):
        super(Del, self).__init__('del', False, *children, **attributes)

class Details(_Element):
    """Represents an HTML details element."""

    def __init__(self, *children, **attributes):
        super(Details, self).__init__('details', False, *children, **attributes)

class Dfn(_Element):
    """Represents an HTML dfn element."""

    def __init__(self, *children, **attributes):
        super(Dfn, self).__init__('dfn', False, *children, **attributes)

class Dialog(_Element):
    """Represents an HTML dialog element."""

    def __init__(self, *children, **attributes):
        super(Dialog, self).__init__('dialog', False, *children, **attributes)

class Div(_Element):
    """Represents an HTML div element."""

    def __init__(self, *children, **attributes):
        super(Div, self).__init__('div', False, *children, **attributes)

class Dl(_Element):
    """Represents an HTML dl element."""

    def __init__(self, *children, **attributes):
        super(Dl, self).__init__('dl', False, *children, **attributes)

class Dt(_Element):
    """Represents an HTML dt element."""

    def __init__(self, *children, **attributes):
        super(Dt, self).__init__('dt', False, *children, **attributes)

class Em(_Element):
    """Represents an HTML em element."""

    def __init__(self, *children, **attributes):
        super(Em, self).__init__('em', False, *children, **attributes)

class Embed(_Element):
    """Represents an HTML embed element."""

    def __init__(self, *children, **attributes):
        super(Embed, self).__init__('embed', True, *children, **attributes)

class Fieldset(_Element):
    """Represents an HTML fieldset element."""

    def __init__(self, *children, **attributes):
        super(Fieldset, self).__init__('fieldset', False, *children, **attributes)

class Footer(_Element):
    """Represents an HTML footer element."""

    def __init__(self, *children, **attributes):
        super(Footer, self).__init__('footer', False, *children, **attributes)

class Form(_Element):
    """Represents an HTML form element."""

    def __init__(self, *children, **attributes):
        super(Form, self).__init__('form', False, *children, **attributes)

class Frame(_Element):
    """Represents an HTML frame element."""

    def __init__(self, *children, **attributes):
        super(Frame, self).__init__('frame', True, *children, **attributes)

class Frameset(_Element):
    """Represents an HTML frameset element."""

    def __init__(self, *children, **attributes):
        super(Frameset, self).__init__('frameset', False, *children, **attributes)

class H1(_Element):
    """Represents an HTML h1 element."""

    def __init__(self, *children, **attributes):
        super(H1, self).__init__('h1', False, *children, **attributes)

class H2(_Element):
    """Represents an HTML h2 element."""

    def __init__(self, *children, **attributes):
        super(H2, self).__init__('h2', False, *children, **attributes)

class H3(_Element):
    """Represents an HTML h3 element."""

    def __init__(self, *children, **attributes):
        super(H3, self).__init__('h3', False, *children, **attributes)

class H4(_Element):
    """Represents an HTML h4 element."""

    def __init__(self, *children, **attributes):
        super(H4, self).__init__('h4', False, *children, **attributes)

class H5(_Element):
    """Represents an HTML h5 element."""

    def __init__(self, *children, **attributes):
        super(H5, self).__init__('h5', False, *children, **attributes)

class H6(_Element):
    """Represents an HTML h6 element."""

    def __init__(self, *children, **attributes):
        super(H6, self).__init__('h6', False, *children, **attributes)

class Head(_Element):
    """Represents an HTML head element."""

    def __init__(self, *children, **attributes):
        super(Head, self).__init__('head', False, *children, **attributes)

class Header(_Element):
    """Represents an HTML header element."""

    def __init__(self, *children, **attributes):
        super(Header, self).__init__('header', False, *children, **attributes)

class Hr(_Element):
    """Represents an HTML hr element."""

    def __init__(self, *children, **attributes):
        super(Hr, self).__init__('hr', True, *children, **attributes)

class Html(_Element):
    """Represents an HTML html element."""

    def __init__(self, *children, **attributes):
        super(Html, self).__init__('html', False, *children, **attributes)

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

    def __init__(self, *children, **attributes):
        super(I, self).__init__('i', False, *children, **attributes)

class Iframe(_Element):
    """Represents an HTML iframe element."""

    def __init__(self, *children, **attributes):
        super(Iframe, self).__init__('iframe', False, *children, **attributes)

class Img(_Element):
    """Represents an HTML img element."""

    def __init__(self, *children, **attributes):
        super(Img, self).__init__('img', True, *children, **attributes)

class Input(_Element):
    """Represents an HTML input element."""

    def __init__(self, *children, **attributes):
        super(Input, self).__init__('input', True, *children, **attributes)

class Ins(_Element):
    """Represents an HTML ins element."""

    def __init__(self, *children, **attributes):
        super(Ins, self).__init__('ins', False, *children, **attributes)

class Keygen(_Element):
    """Represents an HTML keygen element."""

    def __init__(self, *children, **attributes):
        super(Keygen, self).__init__('keygen', True, *children, **attributes)

class Kbd(_Element):
    """Represents an HTML kbd element."""

    def __init__(self, *children, **attributes):
        super(Kbd, self).__init__('kbd', False, *children, **attributes)

class Label(_Element):
    """Represents an HTML label element."""

    def __init__(self, *children, **attributes):
        super(Label, self).__init__('label', False, *children, **attributes)

class Legend(_Element):
    """Represents an HTML legend element."""

    def __init__(self, *children, **attributes):
        super(Legend, self).__init__('legend', False, *children, **attributes)

class Li(_Element):
    """Represents an HTML li element."""

    def __init__(self, *children, **attributes):
        super(Li, self).__init__('li', False, *children, **attributes)

class Link(_Element):
    """Represents an HTML link element."""

    def __init__(self, *children, **attributes):
        super(Link, self).__init__('link', True, *children, **attributes)

class Meta(_Element):
    """Represents an HTML meta element."""

    def __init__(self, *children, **attributes):
        super(Meta, self).__init__('meta', True, *children, **attributes)

class Meter(_Element):
    """Represents an HTML meter element."""

    def __init__(self, *children, **attributes):
        super(Meter, self).__init__('meter', False, *children, **attributes)

class Map(_Element):
    """Represents an HTML map element."""

    def __init__(self, *children, **attributes):
        super(Map, self).__init__('map', False, *children, **attributes)

class Noframes(_Element):
    """Represents an HTML noframes element."""

    def __init__(self, *children, **attributes):
        super(Noframes, self).__init__('noframes', False, *children, **attributes)

class Noscript(_Element):
    """Represents an HTML noscript element."""

    def __init__(self, *children, **attributes):
        super(Noscript, self).__init__('noscript', False, *children, **attributes)

class Object(_Element):
    """Represents an HTML object element."""

    def __init__(self, *children, **attributes):
        super(Object, self).__init__('object', False, *children, **attributes)

class Ol(_Element):
    """Represents an HTML ol element."""

    def __init__(self, *children, **attributes):
        super(Ol, self).__init__('ol', False, *children, **attributes)

class Optgroup(_Element):
    """Represents an HTML optgroup element."""

    def __init__(self, *children, **attributes):
        super(Optgroup, self).__init__('optgroup', False, *children, **attributes)

class Option(_Element):
    """Represents an HTML option element."""

    def __init__(self, *children, **attributes):
        super(Option, self).__init__('option', False, *children, **attributes)

class Output(_Element):
    """Represents an HTML output element."""

    def __init__(self, *children, **attributes):
        super(Output, self).__init__('output', False, *children, **attributes)

class P(_Element): # pylint: disable=invalid-name
    """Represents an HTML p element."""

    def __init__(self, *children, **attributes):
        super(P, self).__init__('p', False, *children, **attributes)

class Param(_Element):
    """Represents an HTML param element."""

    def __init__(self, *children, **attributes):
        super(Param, self).__init__('param', True, *children, **attributes)

class Pre(_Element):
    """Represents an HTML pre element."""

    def __init__(self, *children, **attributes):
        super(Pre, self).__init__('pre', False, *children, **attributes)

class Progress(_Element):
    """Represents an HTML progress element."""

    def __init__(self, *children, **attributes):
        super(Progress, self).__init__('progress', False, *children, **attributes)

class Rp(_Element):
    """Represents an HTML rp element."""

    def __init__(self, *children, **attributes):
        super(Rp, self).__init__('rp', False, *children, **attributes)

class Rt(_Element):
    """Represents an HTML rt element."""

    def __init__(self, *children, **attributes):
        super(Rt, self).__init__('rt', False, *children, **attributes)

class Ruby(_Element):
    """Represents an HTML ruby element."""

    def __init__(self, *children, **attributes):
        super(Ruby, self).__init__('ruby', False, *children, **attributes)

class Q(_Element): # pylint: disable=invalid-name
    """Represents an HTML q element."""

    def __init__(self, *children, **attributes):
        super(Q, self).__init__('q', False, *children, **attributes)

class Samp(_Element):
    """Represents an HTML samp element."""

    def __init__(self, *children, **attributes):
        super(Samp, self).__init__('samp', False, *children, **attributes)

class Script(_Element):
    """Represents an HTML script element."""

    def __init__(self, *children, **attributes):
        super(Script, self).__init__('script', False, *children, **attributes)

class Select(_Element):
    """Represents an HTML select element."""

    def __init__(self, *children, **attributes):
        super(Select, self).__init__('select', False, *children, **attributes)

class Small(_Element):
    """Represents an HTML small element."""

    def __init__(self, *children, **attributes):
        super(Small, self).__init__('small', False, *children, **attributes)

class Source(_Element):
    """Represents an HTML source element."""

    def __init__(self, *children, **attributes):
        super(Source, self).__init__('source', True, *children, **attributes)

class Span(_Element):
    """Represents an HTML span element."""

    def __init__(self, *children, **attributes):
        super(Span, self).__init__('span', False, *children, **attributes)

class Strong(_Element):
    """Represents an HTML strong element."""

    def __init__(self, *children, **attributes):
        super(Strong, self).__init__('strong', False, *children, **attributes)

class Style(_Element):
    """Represents an HTML style element."""

    def __init__(self, *children, **attributes):
        super(Style, self).__init__('style', False, *children, **attributes)

class Sub(_Element):
    """Represents an HTML sub element."""

    def __init__(self, *children, **attributes):
        super(Sub, self).__init__('sub', False, *children, **attributes)

class Summary(_Element):
    """Represents an HTML summary element."""

    def __init__(self, *children, **attributes):
        super(Summary, self).__init__('summary', False, *children, **attributes)

class Sup(_Element):
    """Represents an HTML sup element."""

    def __init__(self, *children, **attributes):
        super(Sup, self).__init__('sup', False, *children, **attributes)

class Table(_Element):
    """Represents an HTML table element."""

    def __init__(self, *children, **attributes):
        super(Table, self).__init__('table', False, *children, **attributes)

class Tbody(_Element):
    """Represents an HTML tbody element."""

    def __init__(self, *children, **attributes):
        super(Tbody, self).__init__('tbody', False, *children, **attributes)

class Td(_Element):
    """Represents an HTML td element."""

    def __init__(self, *children, **attributes):
        super(Td, self).__init__('td', False, *children, **attributes)

class Textarea(_Element):
    """Represents an HTML textarea element."""

    def __init__(self, *children, **attributes):
        super(Textarea, self).__init__('textarea', False, *children, **attributes)

class Tfoot(_Element):
    """Represents an HTML tfoot element."""

    def __init__(self, *children, **attributes):
        super(Tfoot, self).__init__('tfoot', False, *children, **attributes)

class Th(_Element):
    """Represents an HTML th element."""

    def __init__(self, *children, **attributes):
        super(Th, self).__init__('th', False, *children, **attributes)

class Thead(_Element):
    """Represents an HTML thead element."""

    def __init__(self, *children, **attributes):
        super(Thead, self).__init__('thead', False, *children, **attributes)

class Time(_Element):
    """Represents an HTML time element."""

    def __init__(self, *children, **attributes):
        super(Time, self).__init__('time', False, *children, **attributes)

class Title(_Element):
    """Represents an HTML title element."""

    def __init__(self, *children, **attributes):
        super(Title, self).__init__('title', False, *children, **attributes)

class Tr(_Element):
    """Represents an HTML tr element."""

    def __init__(self, *children, **attributes):
        super(Tr, self).__init__('tr', False, *children, **attributes)

class Track(_Element):
    """Represents an HTML track element."""

    def __init__(self, *children, **attributes):
        super(Track, self).__init__('track', True, *children, **attributes)

class Tt(_Element):
    """Represents an HTML tt element."""

    def __init__(self, *children, **attributes):
        super(Tt, self).__init__('tt', False, *children, **attributes)

class Ul(_Element):
    """Represents an HTML ul element."""

    def __init__(self, *children, **attributes):
        super(Ul, self).__init__('ul', False, *children, **attributes)

class Var(_Element):
    """Represents an HTML var element."""

    def __init__(self, *children, **attributes):
        super(Var, self).__init__('var', False, *children, **attributes)

class Video(_Element):
    """Represents an HTML video element."""

    def __init__(self, *children, **attributes):
        super(Video, self).__init__('video', False, *children, **attributes)

class Wbr(_Element):
    """Represents an HTML wbr element."""

    def __init__(self, *children, **attributes):
        super(Wbr, self).__init__('wbr', True, *children, **attributes)



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

