# -*- coding: utf-8 -*-

"""Flask frontend component for xwl.me."""

from __future__ import print_function

from os.path import join, dirname, realpath
from functools import wraps

import flask

from ..blueprint import render_markup, pretty_article


APP = flask.Flask(__name__,
                  template_folder=join(dirname(realpath(__file__)), "templates"),
                  static_folder=join(dirname(realpath(__file__)), "static"))

APP.register_blueprint(render_markup.BP)
APP.register_blueprint(pretty_article.BP)


