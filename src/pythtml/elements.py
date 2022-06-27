# -*- coding: utf-8 -*-

"""pythtml elements."""
from typing import Any, Optional
from html import escape
from xml.sax.saxutils import quoteattr
from keyword import kwlist

__all__ = []

class _Element():
    """Base class for HTML elements."""

    # tag must be set in subclasses.
    tag: str
    is_empty = False

    # used for attribute names.
    kwmap = {u'%s_' % kw: str(kw) for kw in kwlist}

    def __init__(self, *children: "_Element", **attributes: Any):
        # Name clashes with keywords are resolved by appending _ as suggested by PEP 8.
        # For example to pass a class attribute as a keyword argument, use
        # class_'foo, bar'.  The trailing underscore will be stripped because 'class' is a
        # keyword, and a class attribute will be added.
        # Attribute names beginning with 'data_' are presumed to be HTML5 data-* attribute
        # names, and so underscores are replaced with dashes.

        super(_Element, self).__init__()
        self._children = [child for child in children if child is not None]

        # strip attributes having value None or False, but allow 0
        self.attributes = {self._attr_name(k) : v
            for k, v in attributes.items()
            if v not in (None, False)
            }

    def _attr_name(self, name: str):
        """ Implements attribute name conventions."""

        return name.replace(u'_', u'-') if name.startswith(u'data_') else self.kwmap.get(name, name)

    def _generate_attrs(self):
        """ Generates attribute strings."""

        #if isinstance(attr_value, bool), then I assume that __init__ filtered out attributes.
        # with value False.
        return u' '.join([attr_name if isinstance(attr_value, bool)
            else '%s=%s' % (attr_name, quoteattr(str(attr_value)))
            for attr_name, attr_value in self.attributes.items()])

    def __str__(self):
        return ('<!DOCTYPE html>\n<%s%s%s>%s</%s>'
            if self.tag == 'html' else u'<%s%s%s>%s</%s>') % (
            self.tag,
            ' ' if self.attributes else '',
            self._generate_attrs(),
            ''.join([str(child) for child in self._children]),
            self.tag
            )

    def children(self, tag: Optional[str]=None):
        """Returns a list of all children in the order added.
        If tag is not None, then the list is filtered by tag."""

        return [x for x in self._children if tag is None or getattr(x, 'tag', None) == tag]

    def append(self, child: "_Element"):
        """Appends child element."""

        if child is None:
            return

        self._children.append(child)

    def insert(self, offset: int, child: "_Element"):
        """Inserts child element at offset."""

        if child is None:
            return

        self._children.insert(offset, child)

    def remove(self, child: "_Element"):
        """Removes child element from children, if present."""

        self._children = [x for x in self._children if x != child]

    def find_by_id(self, value: Any) -> Optional["_Element"]:
        """Finds the element in the tree having attribute id="value", if present.
        Some so-called "full stack developers" think it's okay to have multiple elements
        with the same id value. This method does not support that."""

        if self.attributes.get('id') == value: # pylint: disable=no-else-return
            return self
        else:
            for child in self._children:
                element = child.find_by_id(value)
                if element:
                    break
            else:
                element = None
            return element

class _EmptyElement(_Element):
    """Base class for HTML empty elements."""

    is_empty = True

    def __init__(self, **attributes: Any): # pylint: disable=useless-super-delegation
        super(_EmptyElement, self).__init__(**attributes)

    def __str__(self):
        return u'<%s%s%s>' % (self.tag, ' ' if self.attributes else '', self._generate_attrs())

class Raw(_Element):
    """Pseudo-element representing raw data."""

    def __init__(self, data: str, *, escape_data: bool=False):
        """Set escape_data to True to escape some reserved HTML characters in data."""

        super().__init__()
        self.data = escape(str(data), quote=False) if escape_data else str(data)

    def __str__(self):
        return self.data


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


class Area(_EmptyElement):
    """Represents an HTML area element."""

    tag = 'area'


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


class Col(_EmptyElement):
    """Represents an HTML col element."""

    tag = 'col'



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


class Embed(_EmptyElement):
    """Represents an HTML embed element."""

    tag = 'embed'



class Fieldset(_Element):
    """Represents an HTML fieldset element."""

    tag = 'fieldset'


class Footer(_Element):
    """Represents an HTML footer element."""

    tag = 'footer'


class Form(_Element):
    """Represents an HTML form element."""

    tag = 'form'

class Frame(_EmptyElement):
    """Represents an HTML frame element."""

    tag = 'frame'



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

    def __init__(self, head: Head, body: Body, *, encoding: str='utf-8', **attributes: Any):
        if head is None:
            raise ValueError('head element must not be None.')
        self.head = head
        if body is None:
            raise ValueError('body element must not be None.')
        self.body = body

        super(Html, self).__init__(head, body, **attributes)
        self.encoding = encoding

    def _charset_meta(self):
        """Returns meta element with charset attribute, if present, or None."""
        head = self.head
        meta_elements = head.children(tag='meta')
        charset_elements = [x for x in meta_elements if 'charset' in x.attributes]
        # there really should be at most one.
        return charset_elements[0] if charset_elements else None

    @property
    def encoding(self):
        """Gets/sets encoding property."""
        charset_meta = self._charset_meta()
        # encoding setter should have been invoked in __init__, and thus a META element with
        # charset attribute should exist.
        assert charset_meta
        return charset_meta.attributes['charset']

    @encoding.setter
    def encoding(self, value: str):
        charset_meta = self._charset_meta()
        if charset_meta:
            charset_meta.attributes['charset'] = value
        else:
            self.head.insert(0, Meta(charset=value))

    def __bytes__(self):
        return self.__str__().encode(self.encoding)

class I(_Element): # pylint: disable=invalid-name
    """Represents an HTML i element."""

    tag = 'i'


class Iframe(_Element):
    """Represents an HTML iframe element."""

    tag = 'iframe'


class Img(_EmptyElement):
    """Represents an HTML img element."""

    tag = 'img'



class Input(_EmptyElement):
    """Represents an HTML input element."""

    tag = 'input'



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


class Link(_EmptyElement):
    """Represents an HTML link element."""

    tag = 'link'



class Meta(_EmptyElement):
    """Represents an HTML meta element."""

    tag = 'meta'



class Meter(_EmptyElement):
    """Represents an HTML meter element."""

    tag = 'meter'



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


class Param(_EmptyElement):
    """Represents an HTML param element."""

    tag = 'param'



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


class Source(_EmptyElement):
    """Represents an HTML source element."""

    tag = 'source'



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


class Track(_EmptyElement):
    """Represents an HTML track element."""

    tag = 'track'



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


class Wbr(_EmptyElement):
    """Represents an HTML wbr element."""

    tag = 'wbr'
