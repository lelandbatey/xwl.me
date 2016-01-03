# -*- coding: utf-8 -*-

"""Rendering ReStructuredText from the contents of the data at a url."""

from __future__ import print_function

from docutils.core import publish_string
import requests


class RstRender(object):
    """Get's the text at a given URL then renders that text as Markdown to
    HTML."""
    def __init__(self, url=None):
        self.url = url
    def html(self, url=None):
        if url is None:
            if self.url:
                url = self.url
            else:
                raise ValueError("No url provided")
        # Don't make requests to large urls
        content_length = int(request.head(url).headers['content-length'])
        if content_length > 100000000:
            raise ValueError("Url source is too large.")
        req = requests.get(url)
        content = publish_string(req.text, writer_name='html')
        return content

