# -*- coding: utf-8 -*-

"""Flask frontend component for xwl.me."""

from __future__ import print_function

from os.path import join, dirname, realpath
from base64 import decodestring

import flask

from ..blueprint import render_markup, pretty_article


APP = flask.Flask(__name__,
                  template_folder=join(dirname(realpath(__file__)), "templates"),
                  static_folder=join(dirname(realpath(__file__)), "static"))

APP.register_blueprint(render_markup.BP)
APP.register_blueprint(pretty_article.BP)


@APP.route('/')
def home():
    """Render the frontpage"""
    return flask.render_template('frontpage.html')

@APP.route('/favicon.ico')
def handle_favicon():
    """Return "x" icon for requested favicons; prevents errors."""
    favicon = "AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAAAAAAAAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD//wAA//8AAP//AADP8wAA5+cAAPPPAAD5nwAA/D8AAPw/AAD5nwAA888AAOfnAADP8wAA//8AAP//AAD//wAA"
    favicon = decodestring(favicon)
    return favicon
