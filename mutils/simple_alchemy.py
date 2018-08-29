# -*- mode: python; coding: utf-8 -*-
"""Very simple, SQLAlchemy table and session makers.
"""

import os
import atexit

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def get_table_class(table_name, schema):
    """`table_name` (str) is used for both the python class name and the `__tablename__`.

    `schema` is a sequence of (`name`, `type`) tuples, `name` being the column name `type`
    being the SQLAlchemy type class to use.
    """

    attrs = dict(
        __tablename__=table_name,
        id=Column(Integer, primary_key=True))

    for row in schema:
        if len(row) == 1 or not row[1]:
            column = row[0]
            type_ = String
        elif isinstance(row, str):
            column = row
            type_ = String
        else:
            column, type_ = row
        attrs[column] = Column(type_)

    return type(table_name, (Base,), attrs)


def get_session(db_path, echo=False):
    """Create and return a SQLAlchemy `session` object
    """

    db_path = os.path.abspath(db_path)
    engine = create_engine('sqlite:///{db_path}'.format(db_path=db_path), echo=echo)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(engine)

    atexit.register(session.close)

    return session
