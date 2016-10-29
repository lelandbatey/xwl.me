# -*- coding: utf-8 -*-

"""Database functionality and sessions."""

from __future__ import print_function

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

import os


def make_engine(path="src_url_database.sqlite3"):
    """Create an SqlAlchemy engine with the given path."""
    return create_engine('sqlite:///'+path)

if 'XWL_DB_PATH' in os.environ:
    engine = make_engine(os.environ['XWL_DB_PATH'])
else:
    engine = make_engine()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

def init_db(base):
    """Creates database with tables, unless they already exist."""
    base.metadata.create_all(engine, checkfirst=True)

