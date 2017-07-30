#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Remove empty elements from an HTML tree."""
from __future__ import print_function
import re

# import requests
from lxml import etree, html
import StringIO
# import bs4

from pprint import pprint

GOOD = type('GOOD', (), {'__repr__': lambda self: 'GOOD',
                         '__nonzero__': lambda self: True})()
BAD = type('BAD', (), {'__repr__': lambda self: 'BAD',
                       '__nonzero__': lambda self: False})()

def has_text(tree, good_map):
    """Returns True if `tree` or any children contain text. Otherwise, returns
    False."""
    retv = False
    try:
        if (tree.text and tree.text.strip()) or tree.tag == 'img':
            good_map[tree] = GOOD
            retv =  True
    except AttributeError:
        pass
    for elem in tree.iterchildren():
        if has_text(elem, good_map):
            good_map[tree] = GOOD
            retv =  True
    if not retv:
        good_map[tree] = BAD
    return retv

def should_delete(elem, good_map, del_map):
    """Records elements that do not contain text that should be deleted.

    An element should be deleted if two conditions are met:
        1. The element does not contain text
        2. The parent of the element does contain text
    """
    retv = False
    parent = elem.getparent()
    if good_map[elem]:
        retv = False
    elif not parent == None and good_map[elem.getparent()]:
        retv = True

    del_map[elem] = retv
    return retv




def remove_empty_elems(tree_str):
    """Remove empty elements from the tree."""
    tree = html.parse(StringIO.StringIO(tree_str))
    good_map = dict()
    del_map = dict()

    has_text(tree.getroot(), good_map)
    for elem in tree.iter():
        should_delete(elem, good_map, del_map)

    root = tree.getroot()
    for elem in del_map:
        if del_map[elem]:
            elem.getparent().remove(elem)
    outstr = StringIO.StringIO()
    tree.write(outstr, encoding="utf-8", pretty_print=True)
    return outstr.getvalue()



if __name__ == "__main__":
    txt = """<div></div>"""
    print(remove_empty_elems(txt))


