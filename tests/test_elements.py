# -*- coding: utf-8 -*-


import sys
import pytest
import uuid

from pyfive.elements import _Element
from pyfive import *

def test_Element_init():
    value = 'foo'
    children = ['foo']
    attributes = {'id': 'bar'}
    
    element = _Element(*children, **attributes)
    assert element.children() == children
    assert element.attributes == attributes


def test_html():
    assert str(Html(Head(), Body())) == '<!DOCTYPE html>\n<html><head><meta charset="utf-8"></head><body></body></html>'

@pytest.mark.parametrize("args", [
    (None, Body()),
    (Head(), None)
    ])
def test_html_bad_args(args):
    with pytest.raises(ValueError):
        Html(*args)

def test_html_encoding_set():
    encoding = 'iso-8859-1'
    html = Html(Head(), Body())
    html.encoding = encoding
    assert html.encoding == encoding

def test_element_str():
    element = Div(Div(P('test', id='foo')))
    assert str(element) == '<div><div><p id="foo">test</p></div></div>'

@pytest.mark.parametrize("input, expected", [
    ('foo', '<p>foo</p>'),
    (43, u'<p>43</p>'),
    (True, u'<p>True</p>'),
    (uuid.UUID('4dc19bc5-af42-4af7-9660-1ce2df9a6005'), u'<p>4dc19bc5-af42-4af7-9660-1ce2df9a6005</p>')
    ])
def test_p(input, expected):
    assert str(P(input)) == expected


def test_html_bytes():
    html = Html(Head(), Body(P('испытание')))
    data = b'<!DOCTYPE html>\n<html><head><meta charset="utf-8"></head><body><p>\xd0\xb8\xd1\x81\xd0\xbf\xd1\x8b\xd1\x82\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5</p></body></html>'
    assert bytes(html) == data

@pytest.mark.parametrize('input, expected', [
    (P('test'), None),
    ('x < y', 'x &lt; y'),
    ])
def test_append(input, expected):
    div = Div()
    div.append(input)
    assert div.children() == [input if expected is None else expected]

def test_append_none():
    div = Div()
    div.append(None)
    assert div.children() == []

def test_insert_none():
    div = Div()
    div.insert(0, None)
    assert div.children() == []

def test_children_tag():
    children = [P(), Div()]
    div = Div(*children)
    assert div.children(tag='p') == children[0:1]

def test_remove():
    children = [P(), Div()]
    div = Div(*children)
    div.remove(children[0])
    assert div.children() == children[1:2]

def test_find_by_id():
    id_element = P(id='foo')
    div = Div(Div(id_element))
    assert div.find_by_id('foo') == id_element

def test_find_by_id_miss():
    id_element = P(id='foo')
    div = Div(Div(id_element))
    assert div.find_by_id('bar') is None

def test_empty_element_str():
    area = Area(shape='circle', coords='75,75,75', href='left.html', alt='Click to go Left')
    assert str(area) == '<area shape="circle" coords="75,75,75" href="left.html" alt="Click to go Left">'

def test_raw():
    assert str(Raw('<script>var x = 1 < 2; var y = x > 1 ? 3 && 5 : 0;</script>')) == '<script>var x = 1 < 2; var y = x > 1 ? 3 && 5 : 0;</script>'

def test_html_head():
    head = Head()
    body = Body()
    html = Html(head, body)
    assert html.head == head

def test_html_body():
    head = Head()
    body = Body()
    html = Html(head, body)
    assert html.body == body

def test_null_child():
    assert str(Div(None)) == '<div></div>'

def test_demangle_kw():
    assert str(Div(class_='foo')) == '<div class="foo"></div>'

def test_demangle_data_attr():
    assert str(Div(data_foo='bar')) == '<div data-foo="bar"></div>'
    
@pytest.mark.parametrize("input, expected", [
    (Div(test='"foo"'), '<div test=\'"foo"\'></div>'),
    (Div(test=1), '<div test="1"></div>'),
    (Script(async_=True), '<script async></script>'),
    (Script(async_=False), '<script></script>'),
    (Script(async_=None), '<script></script>'),
    ])
def test_attribute_quoted(input, expected):
    assert str(input) == expected
