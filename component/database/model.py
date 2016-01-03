# -*- coding: utf-8 -*-
"""Database models."""

from __future__ import print_function

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float

Base = declarative_base()


class SrcUrl(Base):
    """Model for a source url and it's "short_key"."""
    __tablename__ = "md_entry"
    id_num = Column(Integer, primary_key=True)
    short_key = Column(String, unique=True)
    remote_url = Column(String, unique=True)

    def __init__(self, short_key, remote_url):
        self.short_key = short_key
        self.remote_url = remote_url
    @property
    def json(self):
        """Returns json object representation of object."""
        to_return = {}
        to_return['short_key'] = self.short_key
        to_return['remote_url'] = self.remote_url
        to_return['id'] = self.id_num
        return to_return
    def __getstate__(self):
        """Hook for jsonpickle"""
        return self.json
    def __str__(self):
        """String representation"""
        return str(self.json)


