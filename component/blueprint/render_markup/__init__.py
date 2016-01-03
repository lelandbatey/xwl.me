# -*- coding: utf-8 -*-

"""Blueprint for markup language rendering functionality."""

from __future__ import print_function
from os.path import join, dirname, realpath
from functools import wraps

import requests
import flask

from ...database import model, db_session
from ...markdown_render import MarkdownRender
from ...rst_render import RstRender
from ...rand_string import rand_string

BP = flask.Blueprint('render_markup', __name__)

def get_by_shortkey(in_short_url):
    """Returns a SrcUrl with the given `in_short_url`."""
    # Get the full url for the given short key
    entry = db_session.query(
        model.SrcUrl
    ).filter(model.SrcUrl.short_key == in_short_url)
    if entry.count() > 1:
        raise KeyError("Multiple urls with short_key '{}'".format(in_short_url))
    else:
        src_url = entry.first()
        return src_url


@BP.route('/<renderer>/<in_short_url>')
def render(renderer, in_short_url):
    """Render the data at the given short_url as markdown."""
    # Get the appropriate render class
    render_classes = {"md": MarkdownRender,
                      "rs": RstRender}
    if renderer not in render_classes:
        raise ValueError("No render class of the name '{}'".format(renderer))
    lang_renderer = render_classes[renderer]()

    src_url = get_by_shortkey(in_short_url)
    if not src_url:
        return "no source url for given key '{}'".format(in_short_url)
    content = lang_renderer.html(src_url.remote_url)

    return flask.render_template('md.html', content=content)

@BP.route('/add/<path:in_url>')
def add_src_url(in_url):
    """Add a `SrcUrl` entry for the given full path."""
    rand_short_key = rand_string()

    # Prevent submission of urls from this site
    root_url = flask.current_app.config.get('ROOT_URL')
    if root_url in in_url:
        return 'invalid URL'

    # Ghetto fix for auto-decoding of url by flask
    in_url = requests.utils.quote(in_url)
    in_url = in_url.replace("%3A",":")

    # Add a new entry if this URL hasn't been registered, otherwise just use
    # existing entry
    existing_entry = db_session.query(model.SrcUrl).filter(
        model.SrcUrl.remote_url == in_url
    )
    if existing_entry.count() > 1:
        raise KeyError("Multiple entries with remote_url '{}'".format(in_url))
    else:
        existing_entry = existing_entry.first()
    if existing_entry:
        rand_short_key = existing_entry.short_key
    else:
        entry = model.SrcUrl(rand_short_key, in_url)
        db_session.add(entry)
        db_session.commit()

    view_url = flask.url_for('render_markup.render', renderer='md', in_short_url=rand_short_key)
    print(view_url)
    return flask.redirect(view_url, 302)

@BP.route('/list')
def list():
    """List all the url's stored in the database."""
    entries = db_session.query(model.SrcUrl) \
                        .order_by(model.SrcUrl.id_num)
    return flask.render_template('list.html', fullList=entries)


