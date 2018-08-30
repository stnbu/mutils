# -*- mode: python; coding: utf-8 -*-
"""Very simple, SQLAlchemy table and session makers.
"""

import os
import atexit
import inspect

from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import to_instance, TypeEngine

Base = declarative_base()


def get_table_class(table_name, schema, include_id=True):
    """`table_name` (str) is used for both the python class name and the `__tablename__`.

    `schema` is a sequence of (`name`, `type`) tuples, `name` being the column name `type`
    being the SQLAlchemy type class to use.
    """

    attrs = {'__tablename__': table_name}

    if include_id:
        attrs['id'] = Column(Integer, primary_key=True)

    for row in schema:
        kwargs = {}

        if len(row) == 1 or not row[1]:
            column = row[0]
            type_ = String
            args = (type_,)
        elif isinstance(row, str):
            column = row
            type_ = String
            args = (type_,)
        elif inspect.isclass(row[1]) and issubclass(row[1], TypeEngine):
            column, type_ = row
            args = (type_,)
        else:
            column = row[0]
            args, kwargs = row[1]

        attrs[column] = Column(*args, **kwargs)

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
