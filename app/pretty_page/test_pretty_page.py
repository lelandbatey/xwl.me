# -*- coding: utf-8 -*-

from __future__ import print_function
from pprint import pprint

import requests
import bs4

from . import get_body, cull_notext_elems


def test0():
    pprint(get_body("http://www.grosen.dk/jp/Diary_of_a_Disaster.html"))

def test1():
    body = get_body("https://medium.com/civic-technology/rethinking-data-portals-30b66f00585d")
    soup = bs4.BeautifulSoup(body, 'html.parser')
    # cull_notext_elems(soup)
    s1 = soup.prettify().splitlines()
    for elm in soup.descendants:
        try:
            if not (len(elm.get_text()) or elm.get_text().strip()):
                elm.replace_with("")
        except:
            pass
    s2 = soup.prettify().splitlines()
    pprint(set(s2) - set(s1))
    # print(soup.prettify())





if __name__ == "__main__":
    # test0()
    test1()


