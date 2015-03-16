# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals, division, print_function

import sys
import pytest

from pyfive import *
from pyfive.elements import _BaseElement

text = unicode if sys.version_info.major == 2 else str

def test_u_ensure():
    base = _BaseElement()
    value = 'foo'
    u_value = base.u_ensure(value)
    assert isinstance(u_value, base.text) and u_value == value


def test_html():
    assert text(html()) == '<!DOCTYPE html>\n<html></html>'
     
def test_attr():  
    assert text(meta(charset='utf-8')) == '<meta charset="utf-8">'
   
def test_demangle_kw():
    assert text(div(Class='foo')) == '<div class="foo"></div>'
     
def test_demangle_data_attr():
    assert text(div(data_foo='bar')) == '<div data-foo="bar"></div>'
    
def test_demangle_else():
    assert text(div(id='foo')) == '<div id="foo"></div>'
    
def test_demangle_else():
    assert text(div(Id='foo')) == '<div Id="foo"></div>'  
    
def test_attribute_emdash_utf_8():
    em_dash = b'\xe2\x80\x94'
    assert text(div(test=em_dash)) == '<div test="\u2014"></div>'
       
def test_attribute_quoted():
    assert text(div(test='"foo"')) == '<div test=\'"foo"\'></div>'

def test_HTMLAttribute_int():
    assert text(div(test=1)) == '<div test="1"></div>'

def test_HTMLAttribute_unicode_boolean():
    assert text(script(async=True)) == '<script async></script>'

def test_HTMLAttribute_unicode_boolean_false():
    assert text(script(async=False)) == '<script></script>'

def test_raw():
    assert text(body(raw('<script>var x = 1 < 2; var y = x > 1 ? 3 && 5 : 0;</script>'))) == '<body><script>var x = 1 < 2; var y = x > 1 ? 3 && 5 : 0;</script></body>'