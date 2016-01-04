# -*- coding: utf-8 -*-

"""Module for extraction of body of HTML page.

The chief functionality is found in the `get_body` function.

Loosely, uses some imprecise heuristics to attempt to find the top and bottom
of the article, then deletes everything before the start and after the end.
Additionally, many non-content elements are deleted wholesale, such as
`script`, `nav`, `form`, and `button` elements.
The return value is a string representing the prettified page.
"""
from __future__ import print_function
import re

import requests
import bs4

from pprint import pprint


def cull_notext_elems(soup):
    """Removes all elements that do not contain text."""
    has_text = True
    try:
        has_text = soup.get_text().trim()
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

def cull_noncontent(soup):
    """Removes elements that won't contain content. Additionally, removes
    non-content attributes from elements."""
    bad_elems = ['form', 'iframe', 'input', 'button', 'nav', 'canvas', 'style',
            'script', 'option', 'head']
    for elm in soup.find_all(bad_elems):
        elm.replace_with('')
    for elm in soup.descendants:
        if 'attrs' in dir(elm):
            elm.attrs.pop('style', 0)
            elm.attrs.pop('class', 0)
            elm.attrs.pop('id', 0)
    return soup

def find_longest_paragraph(soup, rigorous=True):
    """Searches for the paragraph element with the most text within it. The
    `rigorous` parameter determines whether the to look at p tags that are
    descendants of `li`, `span` and `ul` elements."""
    longest = None
    for elem in soup.find_all('p'):
        if has_tag_parents(elem, ['li', 'ul', 'span']):
            continue
        if longest == None or len(longest.get_text()) < len(elem.get_text()):
            longest = elem
    return longest


def get_body(in_url):
    """Returns main textual body of page."""

    print("in_url:", in_url)
    # Gather the contents of the page.
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0'
    }
    if 'http' not in in_url:
        in_url = 'http://'+in_url
    r = requests.get(in_url, headers=headers)

    soup = bs4.BeautifulSoup(r.text, "html.parser")

    most_children = None
    child_count = 0

    # Removes non-content elements from the tree
    soup = cull_noncontent(soup)

    # Use the 'p' element with the most text as the main heuristic for the body
    # of the article.
    longest = find_longest_paragraph(soup)
    if not longest:
        # Use slightly looser rules for finding the `p` element
        longest = find_longest_paragraph(soup, rigorous=False)
        # If no `p` element can be found, set "longest" to be the whole page
        if not longest:
            longest = soup

    # Remove everything before the first "h1/h2/h3/etc" tag, as that is usually
    # the title of the article. If no `h*` tag is found, nothing is removed.
    expr = re.compile(r'h\d')
    result = soup.find_all(expr)
    if result:
        first_header = result[0]
        remove_before(first_header)

    # Some sites are awesome and wrap the entire article in an "article" tag.
    # On sites like that, we just use the contents of the first "article" tag
    # we find.
    result = soup.find('article')
    if result:
        longest = result
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


