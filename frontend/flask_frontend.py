# -*- coding: utf-8 -*-

"""Flask frontend component for xwl.me."""

from __future__ import print_function
from functools import wraps

import jsonpickle
import flask


# Set encoding options so jsonpickle will pretty-print it's output
jsonpickle.set_preferred_backend('json')
jsonpickle.set_encoder_options('json', sort_keys=True,
                               indent=4, separators=(',', ': '))


APP = flask.Flask(__name__)

def component_register(alias, cls):
    """Registers the given class as a component under
    `APP.config['REGISTERED_COMPONENTS']`."""
    registered = None
    if not 'REGISTERED_COMPONENTS' in APP.config:
        APP.config['REGISTERED_COMPONENTS'] = dict()
    registered = APP.config['REGISTERED_COMPONENTS']
    registered[alias] = cls

def component_get(alias):
    """Returns the class with the given alias."""
    if not 'REGISTERED_COMPONENTS' in APP.config:
        msg = 'No components have been registered; nothing to look up.'
        raise LookupError(msg)
    registered = APP.config['REGISTERED_COMPONENTS']
    return registered[alias]

def components_all_registered(app):
    """Checks that all components given in the set of required components are
    registered."""
    required = app.config['REQUIRED_COMPONENTS']
    registered = app.config['REGISTERED_COMPONENTS']
    missing = sorted(required - set(registered.keys()))
    return bool(len(missing))

def component_require(component_alias):
    """Decorator to register a component as being required for a method. When
    the method is run, if there's not a component registered under
    `component_alias`, raise a `LookupError`."""

    # Register `component_alias` as a required component
    required = None
    if not 'REQUIRED_COMPONENTS' in APP.config:
        APP.config['REQUIRED_COMPONENTS'] = set()
        APP.config['ALL_COMPONENTS_REGISTERED'] = False
    required = APP.config['REQUIRED_COMPONENTS']
    required.add(component_alias)

    def _decorator(func):
        """Since `require_component` is a decorator that takes arguments, it
        must return a function that will be used as a decorator (a sort of
        meta-decorator)."""

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Check all components provided."""
            if not APP.config['ALL_COMPONENTS_REGISTERED']:
                if components_all_registered(APP):
                    msg = 'No component(s) registered for {}'
                    msg.format(missing)
                    raise LookupError(msg)
                else:
                    APP.config['ALL_COMPONENTS_REGISTERED'] = True
            return func(*args, **kwargs)
        return wrapper
    return _decorator



@APP.route('/')
def home():
    """Render the frontpage"""
    return render_template('frontpage.html')




