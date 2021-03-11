from re import match
from unittest.mock import patch
from os import environ

import alembic.config
import psycopg2
import transaction
from unittest import SkipTest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from uuid import uuid4

__all__ = ['DatabaseMixin']


def get_id():
    return uuid4().hex


class DatabaseMixin(object):
    engine_url = 'sqlite:///:memory:'
    __regex = r'postgresql://(?P<user>\w+):(?P<password>\w+)@(?P<host>[\w\d\.]+):(?P<port>\d+)/(?P<dbname>[\w\d\-]+)'

    @classmethod
    def drop_create_database(cls):
        m = match(cls.__regex, cls.engine_url)
        params = m.groupdict()
        dbname = params['dbname']
        del params['dbname']

        with psycopg2.connect(**params) as conn:
            with conn.cursor() as cur:
                conn.autocommit = True
                cur.execute("""SELECT
                                        pg_terminate_backend(pid)
                                    FROM
                                        pg_stat_activity
                                    WHERE
                                        -- don't kill my own connection!
                                        pid <> pg_backend_pid()
                                        ;
                                 """)
                cur.execute(f'DROP DATABASE IF EXISTS "{dbname}";')
                cur.execute(f'CREATE DATABASE "{dbname}";')

    @classmethod
    def database_set_up_class(cls):
        cls.drop_create_database()
        with patch.dict(environ, {'WEB_DATABASE_URL': cls.engine_url}, clear=True):
            alembic.config.main(argv='upgrade head'.split())
        cls.engine = create_engine(cls.engine_url, echo=True)
        cls.session = sessionmaker()

    @classmethod
    def database_tear_down_class(cls):
        cls.session.close_all()
        cls.engine.dispose()
        cls.drop_create_database()

    def database_set_up(self):
        self._connection = self.engine.connect()
        self.trans = self._connection.begin_nested()
        db_session.configure(bind=self._connection)

    def database_tear_down(self):
        self.trans.rollback()
        db_session.remove()
        transaction.abort()
        self._connection.close()

    @classmethod
    def fixture(cls):
        raise SkipTest('TODO')
