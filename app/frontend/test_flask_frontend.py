#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for the process_collection module."""

from __future__ import print_function
import flask_frontend as frontend
import unittest

from pprint import pprint


class RequireTests(unittest.TestCase):
    """Tests for the require_component decorator."""

    def setUp(self):
        """Reload the `frontend` module between each test to reset the state of
        the `APP` variable."""
        reload(frontend)

    def test_variables_created(self):
        """Test that a registration causes the following configuration
        variables to be created within `frontend.APP.config`:
            'REQUIRED_COMPONENTS'
            'ALL_COMPONENTS_REGISTERED'
        """
        # simulate calling a decorator on the definition of a function
        frontend.component_require('test')(lambda x: x)
        conf = sorted(frontend.APP.config.keys())
        self.assertTrue('REQUIRED_COMPONENTS' in conf)
        self.assertTrue('ALL_COMPONENTS_REGISTERED' in conf)

    def test_variables_not_created(self):
        """Test that a registration does not cause the following configuration
        variable to be created within `frontend.APP.config`:
            'REGISTERED_COMPONENTS'
        """
        frontend.component_require('other_test')(lambda x: x)
        conf = sorted(frontend.APP.config.keys())
        self.assertTrue(not 'REGISTERED_COMPONENTS' in conf)
        self.assertRaises

    def test_error_no_registration(self):
        """Calling the decorated function without anything registered raises
        `LookupError`."""
        @frontend.component_require('test_require')
        def func(x):
            return x
        self.assertRaises(LookupError, func)

    def test_registration_alias(self):
        """Registering a class should make that alias appear in
        `frontend.APP.config['REGISTERED_COMPONENTS']`."""
        cls = type('some_class', (), {})
        alias = 'test_alias'
        frontend.component_register(alias, cls)
        
        conf = frontend.APP.config
        registered = sorted(conf['REGISTERED_COMPONENTS'].keys())

        self.assertIn(alias, registered)

    def test_registration_class(self):
        """Registering a class should make that class appear in
        `frontend.APP.config['REGISTERED_COMPONENTS']` under the alias. So not
        only is the alias appearing, but so is the class."""
        cls = type('some_class', (), {})
        alias = 'test_alias'
        frontend.component_register(alias, cls)
        
        conf = frontend.APP.config
        registered = conf['REGISTERED_COMPONENTS']

        self.assertIs(cls, registered[alias])




if __name__ == '__main__':
    unittest.main()


