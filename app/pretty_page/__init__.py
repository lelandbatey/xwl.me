# -*- coding: utf-8 -*-

"""Module for extraction of textual body of HTML page."""
from __future__ import print_function
import re

import requests
import bs4

from pprint import pprint


def cull_notext_elems(soup):
    """Removes all elements that do not contain text."""
    has_text = True
    try:
        has_text = soup.get_text()
    except AttributeError:
        pass

    if not has_text:
        soup.replace_with("")
    else:
        if 'children' in dir(soup):
            for child in soup.children:
                cull_notext_elems(child)

def has_tag_parents(soup, tags):
    """Returns true if a tag has any ancestors with name in the list of given
    names."""
    while soup.parent:
        for tag in tags:
            if soup.parent.name == tag:
                return True
            else:
                continue
        soup = soup.parent
    return False

def remove_after(cur_node):
    """Removes all elements after a certain element."""
    while cur_node.parent:
        after = False
        parent = cur_node.parent
        for node in parent.children:
            if after:
                node.replace_with("")
            elif node is cur_node:
                after = True
        cur_node = parent

def remove_before(cur_node):
    """Removes all elements before the given element."""
    while cur_node.parent:
        after = False
        parent = cur_node.parent
        for node in parent.children:
            if node is cur_node:
                after = True
            if not after:
                node.replace_with("")
        cur_node = parent

def get_body(in_url):
    """Returns main textual body of page."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0'
    }

    if 'http' not in in_url:
        in_url = 'http://'+in_url

    r = requests.get(in_url, headers=headers)
    soup = bs4.BeautifulSoup(r.text, "html.parser")

    most_children = None
    child_count = 0

    # Removes un-necessary things from the data we get
    bad_elems = ['form', 'iframe', 'input', 'button', 'nav', 'canvas', 'style',
            'script', 'option', 'head']
    for elm in soup.find_all(bad_elems):
        elm.replace_with('')
    for elm in soup.descendants:
        if 'attrs' in dir(elm):
            elm.attrs.pop('style', 0)
            elm.attrs.pop('class', 0)

    # Find the 'p' tag with the most text, use that as the main heuristic for
    # article.
    longest = None
    for elem in soup.find_all('p'):
        if has_tag_parents(elem, ['li', 'ul', 'span']):
            continue
        if longest == None or len(longest.get_text()) < len(elem.get_text()):
            longest = elem

    # Remove everything before the first "h1/h2/h3/etc" tag, as that is usually
    # the title of the article
    expr = re.compile(r'h\d')
    if soup.find_all(expr):
        first_header = soup.find_all(expr)[0]
        remove_before(first_header)

    # Some sites are awesome and wrap the entire article in an "article" tag.
    # On sites like that, we just use the contents of the first "article" tag
    # we find.
    if soup.findAll('article'):
        longest = soup.findAll('article')[0]
        # Remove elems which are siblings to the article
        remove_after(longest)

    # Set the root as ancestor node at max 3 above the selected node.
    parent_count = 3
    while parent_count > 0 and longest.parent:
        longest = longest.parent
        parent_count = parent_count - 1
    remove_after(longest)

    # Now that everything unwanted has been removed, return everything else
    while longest.parent:
        longest = longest.parent

    return longest.prettify()


