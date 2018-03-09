# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, division, print_function

import sys
import pytest
import uuid

from pyfive import *
from pyfive.elements import _BaseElement

text = unicode if sys.version_info.major == 2 else str


@pytest.mark.parametrize("input, expected", [
    (u'foo', u'foo'),
    ('test', u'test'),
    (43, '43'),
    (True, 'True'),
    (uuid.UUID('4dc19bc5-af42-4af7-9660-1ce2df9a6005'), '4dc19bc5-af42-4af7-9660-1ce2df9a6005')
    ])
def test_textify(input, expected):
    base = _BaseElement()
    u_value = base.textify(input)
    assert isinstance(u_value, base.text) and u_value == expected


def test_html():
    assert text(Html()) == u'<!DOCTYPE html>\n<html></html>'

@pytest.mark.parametrize("input, expected", [
    (u'foo', u'<p>foo</p>'),
    ('test', u'<p>test</p>'),
    (43, u'<p>43</p>'),
    (True, u'<p>True</p>'),
    (uuid.UUID('4dc19bc5-af42-4af7-9660-1ce2df9a6005'), u'<p>4dc19bc5-af42-4af7-9660-1ce2df9a6005</p>')
    ])
def test_p(input, expected):
    assert text(P(input)) == expected

  
def test_attr():  
    assert text(Meta(charset='utf-8')) == u'<meta charset="utf-8">'
   
def test_demangle_kw():
    assert text(Div(class_='foo')) == '<div class="foo"></div>'
     
def test_demangle_data_attr():
    assert text(Div(data_foo='bar')) == '<div data-foo="bar"></div>'
    
def test_demangle_else():
    assert text(Div(id='foo')) == '<div id="foo"></div>'
    
def test_demangle_else():
    assert text(Div(Id='foo')) == '<div Id="foo"></div>'  
    
def test_attribute_emdash_utf_8():
    em_dash = b'\xe2\x80\x94'
    assert text(Div(test=em_dash)) == '<div test="\u2014"></div>'
       
def test_attribute_quoted():
    assert text(Div(test='"foo"')) == '<div test=\'"foo"\'></div>'

def test_HTMLAttribute_int():
    assert text(Div(test=1)) == '<div test="1"></div>'

def test_HTMLAttribute_unicode_boolean():
    assert text(Script(async=True)) == '<script async></script>'

def test_HTMLAttribute_unicode_boolean_false():
    assert text(Script(async=False)) == '<script></script>'

def test_HTMLAttribute_unicode_boolean_none():
    assert text(Script(async=None)) == '<script></script>'
    
def test_raw():
    assert text(Body(Raw('<script>var x = 1 < 2; var y = x > 1 ? 3 && 5 : 0;</script>'))) == '<body><script>var x = 1 < 2; var y = x > 1 ? 3 && 5 : 0;</script></body>'
    
def test_null_child():
    assert text(Div(None)) == '<div></div>'

def test_name_attribute():
    assert Meta(name='viewport', content='width=1236')
    
def test_html_head_body():
    resource = Html(Head(), Body())
    assert text(resource) == u'<!DOCTYPE html>\n<html><head></head><body></body></html>'

def test_find_self_by_id():
    foo = 'foo'
    element = P(id=foo)
    print(element.attributes)
    assert element.find_by_id(foo) == element

def test_find_child_by_id():
    foo = 'foo'
    id_element = P(id=foo)
    parent = P(id_element)
    assert parent.find_by_id(foo) == id_element
    
def test_append():
    parent = Div()
    child = Div()
    parent.append(child)
    assert parent.children() == [child]
    
def test_children_filtered():
    img = Img()
    children = [u'foo', P(), img, P()]
    parent = Div(*children)
    assert parent.children(tag='img') == [img]

