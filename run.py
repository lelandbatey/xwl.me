# -*- coding: utf-8 -*-
"""Configure WSGI app and run."""

from __future__ import print_function
from app import frontend

APP = frontend.APP
APP.config.update({"ROOT_URL":"http://localhost:5000/"})

if __name__ == '__main__':
	APP.run(debug=True, host="0.0.0.0")
