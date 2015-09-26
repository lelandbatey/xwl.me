from __future__ import print_function
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker


BASE = declarative_base()

class MdEntry(BASE):
    """Holds an entry for a url to a markown document."""
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

class MdModel(object):
    """Model for database holding entries of MdEntries """
    def __init__(self, db_name="remote_md_database.sqlite3"):
        self.db_name = db_name
        self.db = create_engine('sqlite:///'+db_name)
        self.session_class = sessionmaker()
        self.session_class.configure(bind=self.db)
        self.session = self.session_class()
        self.latest_epoch = 0
        # Creates database with tables, unless they already exist.
        MdEntry.metadata.create_all(self.db, checkfirst=True)

    def add_entry(self, short_key, remote_url):
        """Adds an entry with a given short_key and remote_url"""
        entry = MdEntry(short_key, remote_url)
        self.session.add(entry)
        self.session.commit()

    def get_all(self):
        """Returns all the MdEntry objects in order they where stored"""
        entries = self.session.query(MdEntry)\
                      .order_by(MdEntry.id_num)
        return entries

    def get_by_shortkey(self, short_key):
        """ Returns the first MdEntry with the given short_key"""
        entry = self.session.query(MdEntry).filter(
                    MdEntry.short_key == short_key
                )
        if entry.count() > 1:
            raise KeyError("Multiple entries with short_key '{}'".format(short_key))
        else:
            entry = entry.first()
            return entry

    def get_by_remote_url(self, remote_url):
        """ Returns the first MdEntry with the given remote_url"""
        entry = self.session.query(MdEntry).filter(
                    MdEntry.remote_url == remote_url
                )
        if entry.count() > 1:
            raise KeyError("Multiple entries with remote_url '{}'".format(remote_url))
        else:
            entry = entry.first()
            return entry

