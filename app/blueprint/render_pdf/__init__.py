# -*- coding: utf-8 -*-

"""Blueprint for generating pdf from markdown."""

from __future__ import print_function

import flask

from ...pdf_render import make_pdf


BP = flask.Blueprint('render_pdf', __name__)


@BP.route('/md2pdf/', methods=['GET'])
def author_pdf():
    return flask.render_template('md2pdf.html')


@BP.route('/md2pdf/', methods=['POST'])
def create_pdf():
    """Given the form variables 'md_holder' and 'template', returns a
    pandoc-rendered pdf of that markdown."""

    body = flask.request.form['md_holder']
    template = flask.request.form['template']
    if not body:
        return "No text to convert"
    if not template:
        template = 'default'

    response = flask.make_response(make_pdf(body, template))
    response.headers['Content-type'] = "application/pdf"

    return response




