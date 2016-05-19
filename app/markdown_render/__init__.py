# -*- coding: utf-8 -*-

"""Rendering markdown from the contents of the data at a url."""

from __future__ import print_function

from markdown import markdown
import requests


class MarkdownRender(object):
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
        # Don't make requests to large urls. Check the size of a request using
        # an http 'HEAD' request and checking the 'content-length' header of
        # the response. If there's no 'content-length' header, which can happen
        # with chunked responses, assume the content length is zero. Can still
        # lead to requesting overly large files, if those files are served via
        # chunking, but there's no way to check the size of chunked responses
        # ahead of time anyway, so whatever.
        content_length = 0
        head_req = requests.head(url)
        if 'content-length' in head_req.headers:
            content_length = int(head_req.headers['content-length'])

        if content_length > 100000000:
            raise ValueError("Url source is too large.")
        req = requests.get(url)
        md = markdown(req.text)
        return md


