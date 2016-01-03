
# -*- coding: utf-8 -*-

"""Blueprint for markup language rendering functionality."""

from __future__ import print_function

import flask

from ...pretty_page import get_body

BP = flask.Blueprint('pretty_article', __name__)



@BP.route('/<path:in_url>')
def pretty_article(in_url):
    """Render the contents of the main body of the page at the given URL."""
    contents = get_body(in_url)
    return flask.render_template('md.html', content=contents)


