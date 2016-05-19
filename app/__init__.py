
from __future__ import print_function
import traceback

from werkzeug.exceptions import HTTPException
import flask

from . import frontend
APP = frontend.APP

from pprint import pprint

@APP.before_first_request
def setup_logging():
	"""Set up the basic logging configurations."""
	import logging
	from logging import Formatter
	from logging.handlers import RotatingFileHandler

	f_handler = RotatingFileHandler('./log_flask_error.log', maxBytes=1024*1024*20, backupCount=20)
	f_handler.setLevel(logging.INFO)
	f_handler.setFormatter(Formatter('[%(asctime)s] %(levelname)s in %(pathname)s: %(message)s'))

	APP.logger.addHandler(f_handler)

@APP.errorhandler(Exception)
def handle_error(e):
	"""Handle all runtime errors during flask requests by logging them and
	displaying an error message."""
	code = 500
	if isinstance(e, HTTPException):
		code = e.code
	APP.logger.error("Error occurred: {}\n{}".format(e, traceback.format_exc()))
	return flask.jsonify(error=str(e)), code
