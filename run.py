# -*- coding: utf-8 -*-
"""Configure WSGI app and run."""

from __future__ import print_function
from app import frontend

import os

if 'XWL_ROOT_URL' in os.environ:
	ROOT_URL = os.environ['XWL_ROOT_URL']
else:
	ROOT_URL = "http://localhost:5000/"

APP = frontend.APP
APP.config.update({"ROOT_URL":ROOT_URL})

if __name__ == '__main__':
	APP.run(host="0.0.0.0")
